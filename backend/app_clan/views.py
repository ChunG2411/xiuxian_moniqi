from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .serializers import ClanSerializer, RequestClanSerializer, ClanPositionSerializer
from .models import Clan, ClanPosition, RequestClan
from app_user.models import Characters, Money, Bag
from app_item.models import Item, Book
from app_item.serializers import ItemSerializer, BookSerializer
from xiuxian_moniqi.function import f_removeItemfromBag, f_addItemtoBag, f_addBooktoBag


# Create your views here.

@permission_classes([permissions.IsAuthenticated])
class ClanView(APIView):
    def get(self, request):
        clan = Clan.objects.all()
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(clan, request)
        clan_ser = ClanSerializer(page, many=True)
        return pagination.get_paginated_response(clan_ser.data)
    
    def post(self, request):
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        if money.money >= 100000:
            money.money -= 100000
        else:
            return Response("You don't have enough money", status=400)
            
        clan_ser = ClanSerializer(context={"request": request}, data=request.data)
        if clan_ser.is_valid():
            clan_ser.save()
            money.save()
            return Response(clan_ser.data, status=200)
        else:
            return Response(clan_ser.errors, status=400)
    

@permission_classes([permissions.IsAuthenticated])
class ClanDetailView(APIView):
    def get(self, request, id):
        if id == 'current':
            try:
                char = Characters.objects.get(user=request.user)
                position = ClanPosition.objects.get(char=char)
                clan_ser = ClanSerializer(position.clan).data
                clan_ser['position'] = position.position
                return Response(clan_ser, status=200)
            except:
                return Response("Don't have clan", status=400)
        else:
            clan = Clan.objects.get(id=id)
            clan_ser = ClanSerializer(clan)
            return Response(clan_ser.data, status=200)
    
    def put(self, request, id):
        name = request.data.get('name')
        description = request.data.get('description')
        image = request.data.get('image')
        notification = request.data.get('notification')
        leader = request.data.get('leader')

        if id == 'current':
            my_char = Characters.objects.get(user=request.user)
            my_position = ClanPosition.objects.get(char=my_char)
            clan = my_position.clan
        else:
            return Response("Incorrect", status=400)

        if my_position.position != 0:
            return Response("You don't have permission", status=400)
        
        if name:
            clan.name = name
        if description != None:
            clan.description = description
        if image != None:
            clan.image = image
        if notification != None:
            clan.notification = notification
        if leader:
            try:
                char = Characters.objects.get(id=leader)
                position = ClanPosition.objects.get(char=char, clan=clan)
                my_position.position = 1
                position.position = 0
                clan.leader = char
                position.save()
                my_position.save()
            except:
                return Response("Incorrect infor leader", status=400)
        clan.save()

        return Response("Modify successful", status=200)
    
    def delete(self, request, id):
        try:
            Clan.objects.get(id=id).delete()
            return Response("Delete successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def outClan(request, id):
    try:
        clan = Clan.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        clan_position = ClanPosition.objects.get(char=char)
        if clan_position.clan == clan:
            if clan.leader == char:
                clan.delete()
            else:
                clan_position.delete()
                clan.member -= 1
                clan.save()
            return Response("Out clan successful!", status=200)
        else:
            return Response("Isn't member of this clan", status=400)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class RequestClanView(APIView):
    def get(self, request, id):
        request = RequestClan.objects.filter(clan=id)
        request_ser = RequestClanSerializer(request, many=True)
        return Response(request_ser.data, status=200)
    
    def post(self, request, id):
        clan = Clan.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            ClanPosition.objects.get(char=char)
            return Response("You already in another clan", status=400)
        except:
            pass
        try:
            RequestClan.objects.get(char=char, clan=clan)
            return Response("Request already exist!", status=400)
        except:
            RequestClan.objects.create(char=char, clan=clan)
            return Response("Send request successful!", status=200)
    
    def delete(self, request, id):
        clan = Clan.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            RequestClan.objects.get(char=char, clan=clan).delete()
            return Response("Delete request successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def acceptRequest(request, id):
    request_clan = RequestClan.objects.get(id=id)
    clan = Clan.objects.get(id=request_clan.clan.id)
    char = Characters.objects.get(id=request_clan.char.id)
    my_char = Characters.objects.get(user=request.user)
    try:
        my_position = ClanPosition.objects.get(char=my_char)
        if my_position.clan == clan and my_position.position == 0:
            clan.member += 1
            clan.save()
            try:
                clan_position = ClanPosition.objects.get(char=char)
                clan_position.clan = clan
                clan_position.position = 1
                clan_position.save()
            except:
                ClanPosition.objects.create(char=char, clan=clan, position=1)
            request_clan.delete()
            RequestClan.objects.filter(char=char).delete()
            return Response("Accept successful!", status=200)
        else:
            return Response("You don't have permissions!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rejectRequest(request, id):
    request_clan = RequestClan.objects.get(id=id)
    clan = Clan.objects.get(id=request_clan.clan.id)
    my_char = Characters.objects.get(user=request.user)
    try:
        my_position = ClanPosition.objects.get(char=my_char)
        if my_position.clan == clan and my_position.position == 0:
            request_clan.delete()
            return Response("Reject successful!", status=200)
        else:
            return Response("You don't have permissions!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def DedicationView(request, id):
    type = request.data.get('type')
    money_request = request.data.get('money')
    item_request = request.data.get('item')

    char = Characters.objects.get(user=request.user)
    money = Money.objects.get(char=char)
    bag = Bag.objects.get(char=char)
    clan = Clan.objects.get(id=id)

    try:
        ClanPosition.objects.get(char=char, clan=clan)
    except Exception as e:
        return Response(str(e), status=400)

    if type == '1':
        if not money_request:
            return Response('Please insert money', status=400)
        money.money -= int(money_request)
        if money.money < 0:
            return Response("Money not enough!", status=400)
        money.dedication += int(money_request)/2
        money.save()
        clan.exp += int(money_request)/1000
        clan.save()
        return Response({
            'money': money.money,
            'dedication': money.dedication
        }, status=200)
    else:
        if not item_request:
            return Response('Please insert item', status=400)
        try:
            item = Item.objects.get(id=item_request)
            f_removeItemfromBag(bag, item)
            money.dedication += item.price / 2
            money.save()
            clan.exp += item.price/1000
            clan.save()
            return Response({
                'money': money.money,
                'dedication': money.dedication
            }, status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upClan(request, id):
    char = Characters.objects.get(user=request.user)
    clan = Clan.objects.get(id=id)
    position = ClanPosition.objects.get(char=char, clan=clan)
    if position.position == 0:
        if clan.exp >= clan.level * 100:
            clan.exp = 0
            clan.level += 1
            clan.save()
            return Response("Up level clan successful!", status=200)
        else:
            return Response("Exp not enough!", status=400)
    else:
        return Response("You don't have permission!", status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upPosition_Clan(request, id):
    char = Characters.objects.get(user=request.user)
    clan = Clan.objects.get(id=id)
    position = ClanPosition.objects.get(char=char, clan=clan)
    money = Money.objects.get(char=char)

    if position.position == 0:
        return Response("You are leader.", status=400)
    
    if money.dedication >=  position.position*5000:
        money.dedication -= position.position*5000
        money.save()
        position.position += 1
        position.save()
        return Response("Up position successful!", status=200)
    else:
        return Response("Dedication not enough!", status=400)


@permission_classes([permissions.IsAuthenticated])
class MemberClanView(APIView):
    def get(self, request, id):
        all = request.query_params.get('all')

        clan = Clan.objects.get(id=id)
        position = ClanPosition.objects.filter(clan=clan)
        if not all == None:
            return Response(ClanPositionSerializer(position, many=True).data, status=200)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(position, request)
        serializer = ClanPositionSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    def delete(self, request, id):
        char_id = request.query_params.get('char')
        char = Characters.objects.get(id=char_id)
        my_char = Characters.objects.get(user=request.user)
        my_position = ClanPosition.objects.get(char=my_char)
        clan = Clan.objects.get(id=id)
        positon = ClanPosition.objects.get(char=char, clan=clan)

        if my_position.position == 0 or my_position.position >= 6:
            positon.delete()
            clan.member -= 1
            clan.save()
            return Response("Delete member successfull", status=200)
        else:
            return Response("You don't have permission", status=400)


@permission_classes([permissions.IsAuthenticated])
class ClanShopView(APIView):
    def get(self, request, id):
        tab = request.query_params.get('tab')
        type = request.query_params.get('type')

        clan = Clan.objects.get(id=id)
        pagination = PageNumberPagination()
        if tab == '1':
            results = Item.objects.filter(
                            quality__lte=clan.level,
                            level__lte=clan.level)
            if type:
                results = results.filter(type=type)
            page = pagination.paginate_queryset(results, request)
            results_ser = ItemSerializer(page, many=True)
        else:
            results = Book.objects.filter(
                            quality__lte=clan.level,
                            level__lte=clan.level)
            page = pagination.paginate_queryset(results, request)
            results_ser = BookSerializer(page, many=True)

        return pagination.get_paginated_response(results_ser.data)
    
    def post(self, request, id):
        tab = request.data.get('tab')
        item_id = request.data.get('item_id')

        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        bag = Bag.objects.get(char=char)

        if tab == '1':
            item = Item.objects.get(id=item_id)
            money.dedication -= int(item.price/2)
            if money.dedication < 0:
                return Response("Dedication not enough!", status=400)
            f_addItemtoBag(bag, item)
            money.save()
        else:
            item = Book.objects.get(id=item_id)
            money.dedication -= int(item.price/2)
            if money.dedication < 0:
                return Response("Dedication not enough!", status=400)
            f_addBooktoBag(bag, item)
            money.save()
        return Response("Buy successful!", status=200)
        