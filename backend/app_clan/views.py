from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from .serializers import ClanSerializer, RequestClanSerializer, OnlineClanSerializer
from .models import Clan, ClanPosition, RequestClan, OnlineClan
from app_user.models import Characters, Money, Bag
from app_item.views import removeItemfromBag_function, addItemtoBag_function, addBooktoBag_function
from app_item.models import Item, Book
from app_item.serializers import ItemSerializer

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
class ClanView(APIView):
    def get(self, request):
        clan = Clan.objects.all()
        clan_ser = ClanSerializer(clan, many=True)
        return Response(clan_ser.data, status=200)
    
    def post(self, request):
        try:
            clan_ser = ClanSerializer(context={"request": request}, data=request.data)
            if clan_ser.is_valid():
                clan_ser.save()
                return Response(clan_ser.data, status=201)
            else:
                return Response(clan_ser.errors, status=400)
        except Exception as e:
            return Response(str(e), status=400)
    

@permission_classes([permissions.IsAuthenticated])
class ClanDetailView(APIView):
    def get(self, request, id):
        try:
            clan = Clan.objects.get(id=id)
            clan_ser = ClanSerializer(clan)
            return Response(clan_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
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
    try:
        request_clan = RequestClan.objects.get(id=id)
        clan = Clan.objects.get(id=request_clan.clan.id)
        char = Characters.objects.get(id=request_clan.char.id)
        my_char = Characters.objects.get(user=request.user)
        try:
            my_position = ClanPosition.objects.get(char=my_char)
            if my_position.clan == clan and my_position.position == 10:
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
                return Response("Accept successful!", status=200)
            else:
                return Response("You don't have permissions!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rejectRequest(request, id):
    try:
        request_clan = RequestClan.objects.get(id=id)
        clan = Clan.objects.get(id=request_clan.clan.id)
        my_char = Characters.objects.get(user=request.user)
        try:
            my_position = ClanPosition.objects.get(char=my_char)
            if my_position.clan == clan and my_position.position == 10:
                request_clan.delete()
                return Response("Reject successful!", status=200)
            else:
                return Response("You don't have permissions!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        
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
        if clan.exp > 100:
            clan.exp = 100
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
            bag.items[str(item.id)]
            removeItemfromBag_function(bag, item)
            money.dedication += item.price / 2
            money.save()
            clan.exp += item.price/1000
            if clan.exp > 100:
                clan.exp = 100
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
    try:
        char = Characters.objects.get(user=request.user)
        clan = Clan.objects.get(id=id)
        position = ClanPosition.objects.get(char=char, clan=clan)
        if position.position == 10:
            if clan.exp == clan.exp_request:
                clan.exp = 0
                clan.level += 1
                clan.exp_request = clan.level*100
                clan.save()
                return Response("Up level clan successful!", status=200)
            else:
                return Response("Exp not enough!", status=400)
        else:
            return Response("You don't have permission!", status=400)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upPosition(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        clan = Clan.objects.get(id=id)
        position = ClanPosition.objects.get(char=char, clan=clan)
        money = Money.objects.get(char=char)

        if money.dedication >=  position.position*5000:
            money.dedication -= position.position*5000
            money.save()
            position.position += 1
            position.save()
            return Response("Up position successful!", status=200)
        else:
            return Response("Dedication not enough!", status=400)
    except Exception as e:
        return Response(str(e), status=400)
    

@permission_classes([permissions.IsAuthenticated])
class ClanShopView(APIView):
    def get(self, request, id):
        type = request.query_params.get('type')
        clan = Clan.objects.get(id=id)
        if type:
            items = Item.objects.filter(type=type, quality__lte=clan.level)
        else:
            items = Item.objects.filter(quality__lte=clan.level)
        item_ser = ItemSerializer(items, many=True)
        return Response(item_ser.data, status=200)
    
    def post(self, request, id):
        type = request.data.get('type')
        item_id = request.data.get('item_id')

        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        bag = Bag.objects.get(char=char)

        if type == '1':
            item = Item.objects.get(id=item_id)
            money.dedication -= item.price*2
            if money.dedication < 0:
                return Response("Dedication not enough!", status=400)
            addItemtoBag_function(bag, item)
            money.save()
        else:
            item = Book.objects.get(id=item_id)
            money.dedication -= item.price*2
            if money.dedication < 0:
                return Response("Dedication not enough!", status=400)
            addBooktoBag_function(bag, item)
            money.save()
        return Response("Buy successful!", status=200)
        

@permission_classes([permissions.IsAuthenticated])
class OnlineClanView(APIView):
    def get(self, request, id):
        clan = Clan.objects.get(id=id)
        try:
            online = OnlineClan.objects.get(clan=clan)
        except:
            online = OnlineClan.objects.create(clan=clan)
        online_ser = OnlineClanSerializer(online)
        return Response(online_ser.data, status=200)

    def post(self, request, id):
        char = Characters.objects.get(user=request.user)
        clan = Clan.objects.get(id=id)
        online = OnlineClan.objects.get(clan=clan)
        online.char.add(char)
        online.save()
        return Response("Join successful!", status=200)
    
    def delete(self, request, id):
        char = Characters.objects.get(user=request.user)
        clan = Clan.objects.get(id=id)
        online = OnlineClan.objects.get(clan=clan)
        online.char.remove(char)
        online.save()
        return Response("Out successful!", status=200)
