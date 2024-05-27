from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

from .serializers import OrganizationSerializer, LocalitySerializer, MineSerializer, MarketSerializer, MailSerializer
from .models import Organization, Locality, Mine, Market, Mail
from app_user.models import Characters, Money, Properties
from xiuxian_moniqi.config import LOCALITY, MINE,MARKET

from datetime import datetime, timedelta

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
            char = Characters.objects.get(user=request.user)
            try:
                locality = Locality.objects.get(char=char)
            except:
                return Response("Create locality first", status=400)

            if locality.organization:
                organization = locality.organization
                organization_ser = OrganizationSerializer(organization)
                return Response(organization_ser.data, status=200)
            else:
                return Response("Don't have organization", status=400)
        else:
            organization = Organization.objects.get(id=id)
            organization_ser = OrganizationSerializer(organization)
            return Response(organization_ser.data, status=200)
    
    def patch(self, request, id):
        if id == 'current':
            char = Characters.objects.get(user=request.user)
            my_locality = Locality.objects.get(char=char)
            localities = Locality.objects.filter(organization=my_locality.organization).exclude(char=char)

            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(localities, request)
            response = [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.char.name
                } for i in page
            ]
            response.append({
                    'id': str(my_locality.id),
                    'name': my_locality.name,
                    'level': my_locality.level,
                    'owner': my_locality.char.name
                })
            return pagination.get_paginated_response(response)
        else:
            return Response("You don't have permission", status=400)
        
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
        if locality.organization:
            return Response('You in another organization', status=400)
        
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
        mine.defender = mine.level * MINE['defender']
        mine.time_protect = None
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
            mine.get_at = datetime.now(timezone.get_current_timezone())
            mine.save()
            return Response("Collect successfull", status=200)
        else:
            diff = mine.level * MINE['defender'] - mine.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            mine.defender = mine.level * MINE['defender']
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
        market.defender = market.level * MARKET['defender']
        market.time_protect = None
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
            market.get_at = datetime.now(timezone.get_current_timezone())
            market.save()
            return Response("Collect successfull", status=200)
        else:
            diff = market.level * MARKET['defender'] - market.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            market.defender = market.level * MARKET['defender']
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
            'owner': str(locality.id),
            'locality': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.char.name
                } for i in localities
            ],
            'mine': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.owner.name if i.owner else None
                } for i in mines
            ],
            'market': [
                {
                    'id': str(i.id),
                    'name': i.name,
                    'level': i.level,
                    'owner': i.owner.name if i.owner else None
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
    
    def put(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        locality = Locality.objects.get(char=char)
        locality.name = name
        locality.save()
        return Response("Modify successful", status=200)
    
    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        locality = Locality.objects.get(char=char)
        if locality.organization:
            locality.organization.member -= 1
            locality.organization.save()
        locality.delete()
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
            'owner': str(locality.id),
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
            diff = locality.level * LOCALITY['defender'] - locality.defender
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            locality.defender = locality.level * LOCALITY['defender']
            locality.save()
            return Response("Restore difender successfull", status=200)
        
        if power:
            diff = locality.level * LOCALITY['power'] - locality.power
            if money.money < diff * 10:
                return Response("You dont enough money", status=400)
            money.money -= diff * 10
            money.save()
            locality.power = locality.level * LOCALITY['power']
            locality.save()
            return Response("Restore power successfull", status=200)
        
        if level:
            if money.money < locality.level * 20000:
                return Response("You dont enough money", status=400)
            money.money -= locality.level * 20000
            money.save()
            locality.level += 1
            locality.defender += LOCALITY['defender']
            locality.power += LOCALITY['power']
            locality.save()
            return Response("Up level successfull", status=200)
        return Response("", status=200)


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def attackMine(request, id):
    mine = Mine.objects.get(id=id)
    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    money = Money.objects.get(char=char)
    locality = Locality.objects.get(char=char)
    
    if money.money < locality.power:
        return Response("You dont enough money", status=400)
    
    now = datetime.now(timezone.get_current_timezone())
    if mine.time_protect and now < mine.time_protect:
        return Response("Mine in time protect", status=400)
    
    if locality.power < mine.defender:
        defender_left = mine.defender - locality.power
        money.money -= locality.power
        mine.defender -= locality.power + properties.power
        if mine.defender < 0:
            mine.defender = 0
        money.save()
        locality.power = 0
        locality.save()
        if defender_left > properties.power:
            mine.time_protect = now + timedelta(days=1)
            mine.save()
            return Response("Attack fail", status=400)
        else:
            mine.owner = locality
            mine.time_protect = now + timedelta(days=1)
            mine.save()
            return Response("Attack success", status=200)
    else:
        locality.power -= mine.defender
        money.money -= mine.defender
        mine.owner = locality
        mine.defender = 0
        mine.time_protect = now + timedelta(days=1)
        mine.save()
        money.save()
        locality.save()
        return Response("Attack success", status=200)


@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def attackMarket(request, id):
    market = Market.objects.get(id=id)
    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    money = Money.objects.get(char=char)
    locality = Locality.objects.get(char=char)
    
    if money.money < locality.power:
        return Response("You dont enough money", status=400)
    
    now = datetime.now(timezone.get_current_timezone())
    if market.time_protect and now < market.time_protect:
        return Response("Market in time protect", status=400)
    
    if locality.power < market.defender:
        defender_left = market.defender - locality.power
        money.money -= locality.power
        market.defender -= locality.power + properties.power
        if market.defender < 0:
            market.defender = 0
        money.save()
        locality.power = 0
        locality.save()
        if defender_left > properties.power:
            market.time_protect = now + timedelta(days=1)
            market.save()
            return Response("Attack fail", status=400)
        else:
            market.owner = locality
            market.time_protect = now + timedelta(days=1)
            market.save()
            return Response("Attack success", status=200)
    else:
        locality.power -= market.defender
        money.money -= market.defender
        market.owner = locality
        market.defender = 0
        market.time_protect = now + timedelta(days=1)
        market.save()
        money.save()
        locality.save()
        return Response("Attack success", status=200)
    

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def attackLocality(request, id):
    locality = Locality.objects.get(id=id)
    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    money = Money.objects.get(char=char)
    my_locality = Locality.objects.get(char=char)

    if my_locality.organization == locality.organization:
        return Response("Can't attack ally", status=400)

    if money.money < my_locality.power:
        return Response("You dont enough money", status=400)
    
    now = datetime.now(timezone.get_current_timezone())
    if locality.time_protect and now < locality.time_protect:
        return Response("Locality in time protect", status=400)
        
    my_power = my_locality.power + properties.power
    partner_power = locality.defender + locality.power
    if my_power < partner_power:
        diff = locality.defender - my_power
        money.money -= my_locality.power
        money.save()
        if diff > 0:
            locality.defender -= my_power
        else:
            locality.power -= my_power - locality.defender
            locality.defender = 0
        my_locality.power = 0
        my_locality.save()
        locality.time_protect = now + timedelta(days=1)
        locality.save()
        return Response("Attack fail", status=400)
    else:
        diff = partner_power - my_locality.power
        if diff < 0:
            my_locality.power -= partner_power
            money.money -= partner_power
        else:
            money.money -= my_locality.power
            my_locality.power = 0
        money.money += partner_power * 10
        money.save()
        locality.defender = 0
        locality.power = 0
        locality.time_protect = now + timedelta(days=1)
        locality.save()
        my_locality.save()
        return Response("Attack success", status=200)


@permission_classes([permissions.IsAuthenticated])
class MailView(APIView):
    def get(self, request):
        type = request.query_params.get('type')
        char = Characters.objects.get(user=request.user)
        locality = Locality.objects.get(char=char)

        if type == '1':
            mails = Mail.objects.filter(sender=locality)
        else:
            mails = Mail.objects.filter(receiver=locality)

        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(mails, request)
        serializer = MailSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    def post(self, request):
        to = request.data.get('to')
        content = request.data.get('content')

        char = Characters.objects.get(user=request.user)
        my_locality = Locality.objects.get(char=char)
        locality = Locality.objects.get(id=to)
        mail = Mail.objects.create(
            sender = my_locality,
            receiver = locality,
            content = content
        )
        serializer = MailSerializer(mail)
        return Response(serializer.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class MailDetailView(APIView):
    def get(self, request, id):
        mail = Mail.objects.get(id=id)
        serializer = MailSerializer(mail)
        return Response(serializer.data, status=200)
