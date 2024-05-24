from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .serializers import OrganizationSerializer, LocalitySerializer, MineSerializer, MarketSerializer
from .models import Organization, Locality, Mine, Market
from app_user.models import Characters, Money, Properties

# Create your views here.


@permission_classes([permissions.IsAuthenticated])
class OrganizationView(APIView):
    def get(self, request):
        organization = Organization.objects.all()
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(organization, request)
        organization_ser = OrganizationSerializer(page, many=True)
        return pagination.get_paginated_response(organization_ser.data)
    
    def post(self, request):
        organization_ser = OrganizationSerializer(context={"request": request}, data=request.data)
        if organization_ser.is_valid():
            organization_ser.save()
            return Response(organization_ser.data, status=200)
        else:
            return Response(organization_ser.errors, status=400)
    

@permission_classes([permissions.IsAuthenticated])
class OrganizationDetailView(APIView):
    def get(self, request, id):
        if id == 'current':
            try:
                char = Characters.objects.get(user=request.user)
                try:
                    locality = Locality.objects.get(char=char)
                except:
                    return Response("Create locality first", status=400)

                organization = locality.organization
                organization_ser = OrganizationSerializer(organization)
                return Response(organization_ser.data, status=200)
            except:
                return Response("Don't have organization", status=400)
        else:
            organization = Organization.objects.get(id=id)
            organization_ser = OrganizationSerializer(organization)
            return Response(organization_ser.data, status=200)
        
    def delete(self, request, id):
        try:
            Organization.objects.get(id=id).delete()
            return Response("Delete successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def joinOrganization(request, id):
    try:
        organization = Organization.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            locality = Locality.objects.get(char=char)
        except:
            return Response("Create locality first", status=400)

        locality.organization = organization
        organization.member += 1
        organization.save()
        locality.save()
        return Response("Join organization successful!", status=200)

    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def outOrganization(request, id):
    try:
        organization = Organization.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            locality = Locality.objects.get(char=char)
        except:
            return Response("Create locality first", status=400)

        if locality.organization == organization:
            locality.organization = None
            organization.member -= 1
            organization.save()
            locality.save()
            return Response("Out organization successful!", status=200)
        else:
            return Response("Isn't member of this organization", status=400)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class MineView(APIView):
    def get(self, request, id):
        mine = Mine.objects.get(id=id)
        serializer = MineSerializer(mine)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = MineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    def put(self, request):
        id = request.data.get('mine')
        mine = Mine.objects.get(id=id)
        char = Characters.objects.get(user=request.user)

        if mine.owner.char != char:
            return Response("You dont own this mine", status=400)
        mine.owner = None
        mine.save()
        return Response("Remove successfull", status=200)

    def patch(self, request):
        id = request.data.get('mine')
        type = request.data.get('type')

        mine = Mine.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if mine.owner.char != char:
            return Response("You dont own this mine", status=400)
        if type == 'collect':
            money.money += mine.store
            money.save()
            mine.store = 0
            mine.save()
            return Response("Collect successfull", status=200)
        else:
            diff = mine.level * 1000 - mine.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            mine.defender = mine.level * 1000
            mine.save()
            return Response("Restore successfull", status=200)
    
    def delete(self, request, id):
        Mine.objects.get(id=id).delete()
        return Response("Delete successfull", status=200)


@permission_classes([permissions.IsAuthenticated])
class MarketView(APIView):
    def get(self, request, id):
        market = Market.objects.get(id=id)
        serializer = MarketSerializer(market)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    def put(self, request):
        id = request.data.get('market')
        market = Market.objects.get(id=id)
        char = Characters.objects.get(user=request.user)

        if market.owner.char != char:
            return Response("You dont own this market", status=400)
        market.owner = None
        market.save()
        return Response("Remove successfull", status=200)
    
    def patch(self, request):
        id = request.data.get('market')
        type = request.data.get('type')

        market = Market.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if market.owner.char != char:
            return Response("You dont own this market", status=400)
        if type == 'collect':
            money.money += market.store
            money.save()
            market.store = 0
            market.save()
            return Response("Collect successfull", status=200)
        else:
            diff = market.level * 1000 - market.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            market.defender = market.level * 1000
            market.save()
            return Response("Restore successfull", status=200)
    
    def delete(self, request, id):
        Market.objects.get(id=id).delete()
        return Response("Delete successfull", status=200)
    

@permission_classes([permissions.IsAuthenticated])
class LocalityView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        try:
            locality = Locality.objects.get(char=char)
        except:
            return Response("Create locality first", status=400)
        
        level, pos_x, pos_y = locality.level, locality.pos_x, locality.pos_y
        localities = Locality.objects.filter(
            pos_x__lte = pos_x + level * 100,
            pos_x__gte = pos_x - level * 100,
            pos_y__lte = pos_y + level * 100,
            pos_y__gte = pos_y - level * 100
        ).exclude(char = char)
        mines = Mine.objects.filter(
            pos_x__lte = pos_x + level * 100,
            pos_x__gte = pos_x - level * 100,
            pos_y__lte = pos_y + level * 100,
            pos_y__gte = pos_y - level * 100
        )
        markets = Market.objects.filter(
            pos_x__lte = pos_x + level * 100,
            pos_x__gte = pos_x - level * 100,
            pos_y__lte = pos_y + level * 100,
            pos_y__gte = pos_y - level * 100
        )
        return Response({
            'locality': [
                {
                    'id': str(i.id),
                    'name': i.char.name,
                    'level': i.level,
                    'owner': i.char.name
                } for i in localities
            ],
            'mine': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.owner.char.name if i.owner else None
                } for i in mines
            ],
            'market': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.owner.char.name if i.owner else None
                } for i in markets
            ]
        }, status=200)

    def post(self, request):
        locality_ser = LocalitySerializer(context={"request": request}, data=request.data)
        if locality_ser.is_valid():
            locality_ser.save()
            return Response(locality_ser.data, status=200)
        else:
            return Response(locality_ser.errors, status=400)
    
    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        Locality.objects.get(char=char).delete()
        return Response("Delete successfull", status=200)
    

@permission_classes([permissions.IsAuthenticated])
class LocalityDetailView(APIView):
    def get(self, request, id):
        if id == 'current':
            char = Characters.objects.get(user=request.user)
            try:
                locality = Locality.objects.get(char=char)
            except:
                return Response("Create locality first", status=400)
            serializer = LocalitySerializer(locality)
            return Response(serializer.data, status=200)
        else:
            locality = Locality.objects.get(id=id)
            serializer = LocalitySerializer(locality)
            return Response(serializer.data, status=200)
    
    def patch(self, request, id):
        char = Characters.objects.get(user=request.user)
        locality = Locality.objects.get(char=char)
        mines = Mine.objects.filter(owner=locality)
        markets = Market.objects.filter(owner=locality)

        return Response({
            'mine': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level
                } for i in mines
            ],
            'market': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level
                } for i in markets
            ]
        }, status=200)

    def put(self, request, id):
        defender = request.data.get('defender')
        level = request.data.get('level')
        power = request.data.get('power')

        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        locality = Locality.objects.get(char=char)

        if defender:
            diff = locality.level * 1000 - locality.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            locality.defender = locality.level * 1000
            locality.save()
            return Response("Restore difender successfull", status=200)
        
        if power:
            diff = locality.level * 200 - locality.power
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            locality.power = locality.level * 200
            locality.save()
            return Response("Restore power successfull", status=200)
        
        if level:
            if money.money < locality.level * 10000:
                return Response("You dont enough money", status=400)
            money.money -= locality.level * 20000
            money.save()
            locality.level += 1
            locality.defender += 1000
            locality.power += 200
            locality.save()
            return Response("Up level successfull", status=200)
        return Response("", status=200)


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def attackMine(request, id):
    mine = Mine.objects.get(id=id)
    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    locality = Locality.objects.get(char=char)
    
