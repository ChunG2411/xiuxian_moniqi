from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import City, Tower
from .serializers import CitySerializer, TowerSerializer
from app_user.models import Bag, Characters, Properties, Money
from app_item.models import Item
from app_item.serializers import ItemSerializer
from xiuxian_moniqi.function import f_removeItemfromBag, f_addItemtoBag, f_getRandomItem

import random


# Create your views here.

@permission_classes([permissions.IsAuthenticated])
class CityView(APIView):
    def get(self, request):
        city = City.objects.all()
        city_ser = CitySerializer(city, many=True)
        return Response(city_ser.data, status=200)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
class CityDetailView(APIView):
    def get(self, request, id):
        city = City.objects.get(id=id)
        city_ser = CitySerializer(city)
        return Response(city_ser.data, status=200)

    def delete(self, request, id):
        City.objects.get(id=id).delete()
        return Response("Delete city successfull", status=200)


@permission_classes([permissions.IsAuthenticated])
class TowerView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        try:
            tower = Tower.objects.get(char=char)
        except:
            tower = Tower.objects.create(char=char)
        serializer = TowerSerializer(tower)
        return Response(serializer.data, status=200)

    def post(self, request):
        char = Characters.objects.get(user=request.user)
        tower = Tower.objects.get(char=char)
        money = Money.objects.get(char=char)
        bag = Bag.objects.get(char=char)
        property = Properties.objects.get(char=char)

        prize = {
            'money': 0,
            'item': []
        }
        if property.power <= (tower.floor + 1) * 123:
            return Response("Fail", status=400)
        else:
            tower.floor += 1
            money.money += tower.floor * 1000
            prize['money'] = tower.floor * 1000
            tower.save()
            money.save()

            for i in range(tower.floor):
                item = f_getRandomItem('')
                f_addItemtoBag(bag, item)
                prize['item'].append(
                    {
                        'name': item.name,
                        'image': item.image.url,
                        'quality': item.quality
                    }
                )
        return Response(prize, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def FightResult(request):
    type = request.data.get('type')
    char_id = request.data.get('char_id')

    char_1 = Characters.objects.get(user=request.user)
    char_2 = Characters.objects.get(id=char_id)
    pro_1 = Properties.objects.get(char=char_1)
    pro_2 = Properties.objects.get(char=char_2)
    bag_1 = Bag.objects.get(char=char_1)
    bag_2 = Bag.objects.get(char=char_2)
    money_1 = Money.objects.get(char=char_1)
    money_2 = Money.objects.get(char=char_2)

    if pro_1.power <= pro_2.power:
        if type == '0':
            return Response('Lose', status=400)
        else:
            if random.randint(0, 5) != 1:
                rand_money = random.randint(0, 10000)
                if money_1.money - rand_money < 0:
                    money = money_1.money
                    money_2.money += money
                    money_1.money = 0
                    money_1.save()
                    money_2.save()
                    return Response({
                        'money': money,
                        'item': None
                    }, status=400)
                else:
                    money_1.money -= rand_money
                    money_2.money += rand_money
                    money_1.save()
                    money_2.save()
                    return Response({
                        'money': rand_money,
                        'item': None
                    }, status=400)
            else:
                bag_1_item = bag_1.items
                if len(bag_1_item) == 0:
                    return Response({
                        'money': None,
                        'item': None
                    }, status=400)
                index = random.randint(0, len(bag_1_item))
                item_id = list(bag_1_item.keys())[index]
                item = Item.objects.get(id=item_id)
                f_addItemtoBag(bag_2, item)
                f_removeItemfromBag(bag_1, item)
                item_ser = ItemSerializer(item)
                return Response({
                    'money': None,
                    'item': item_ser.data
                }, status=400)
    else:
        if type == '0':
            return Response('Win', status=200)
        else:
            if random.randint(0, 5) != 1:
                rand_money = random.randint(0, 10000)
                if money_2.money - rand_money < 0:
                    money = money_2.money
                    money_1.money += money
                    money_2.money = 0
                    money_1.save()
                    money_2.save()
                    return Response({
                        'money': money,
                        'item': None
                    }, status=200)
                else:
                    money_2.money -= rand_money
                    money_1.money += rand_money
                    money_1.save()
                    money_2.save()
                    return Response({
                        'money': rand_money,
                        'item': None
                    }, status=200)
            else:
                bag_2_item = bag_2.items
                if len(bag_2_item) == 0:
                    return Response({
                        'money': None,
                        'item': None
                    }, status=200)
                index = random.randint(0, len(bag_2_item))
                item_id = list(bag_2_item.keys())[index]
                item = Item.objects.get(id=item_id)
                f_addItemtoBag(bag_1, item)
                f_removeItemfromBag(bag_2, item)
                item_ser = ItemSerializer(item)
                return Response({
                    'money': None,
                    'item': item_ser.data
                }, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def GameResult(request):
    result = request.data.get('result')
    money_request = request.data.get('money')

    char = Characters.objects.get(user=request.user)
    money = Money.objects.get(char=char)
    if result == '0':
        money.money -= int(money_request)
        money.save()
        return Response({'money':money_request}, status=400)
    else:
        money.money += int(money_request)
        money.save()
        return Response({'money':money_request}, status=200)