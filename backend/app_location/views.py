from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from .models import (
    City,
    OnlineCity,
    Tower,
    TowerChallenge,
    ChallengeBoard
    )
from .serializers import (
    CitySerializer,
    OnlineCitySerializer,
    TowerSerializer,
    TowerChallengeSerializer,
    ChallengeBoardSerializer
    )
from app_user.models import Bag, Characters, Properties, Money
from app_item.models import Item
from app_item.serializers import ItemSerializer
from app_item.views import getRandomItem_function, addItemtoBag_function, removeItemfromBag_function

import random

# Create your views here.
@permission_classes([permissions.IsAuthenticated])
class CityView(APIView):
    def get(self, request):
        city = City.objects.all()
        city_ser = CitySerializer(city, many=True)
        return Response(city_ser.data, status=200)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getCityDetail(request, id):
    try:
        city = City.objects.get(id=id)
        city_ser = CitySerializer(city)
        return Response(city_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class OnlineCityView(APIView):
    def get(self, request, id):
        city = City.objects.get(id=id)
        try:
            online = OnlineCity.objects.get(city=city)
        except:
            online = OnlineCity.objects.create(city=city)
        online_ser = OnlineCitySerializer(online)
        return Response(online_ser.data, status=200)

    def post(self, request, id):
        char = Characters.objects.get(user=request.user)
        city = City.objects.get(id=id)
        online = OnlineCity.objects.get(city=city)
        online.char.add(char)
        online.save()
        return Response("Join successful!", status=200)
    
    def delete(self, request, id):
        char = Characters.objects.get(user=request.user)
        city = City.objects.get(id=id)
        online = OnlineCity.objects.get(city=city)
        online.char.remove(char)
        online.save()
        return Response("Out successful!", status=200)
    

@permission_classes([permissions.IsAuthenticated])
class TowerView(APIView):
    def get(self, request):
        tower = Tower.objects.all()
        tower_ser = TowerSerializer(tower, many=True)
        return Response(tower_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getTowerDetail(request, id):
    try:
        tower = Tower.objects.get(id=id)
        tower_ser = TowerSerializer(tower)
        return Response(tower_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class TowerChallengeView(APIView):
    def get(self, request, id):
        tower = Tower.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            challenge = TowerChallenge.objects.get(tower=tower, char=char)
        except:
            challenge = TowerChallenge.objects.create(tower=tower, char=char)
        challenge_ser = TowerChallengeSerializer(challenge)
        return Response(challenge_ser.data, status=200)
    
    def post(self, request, id):
        floor = request.data.get('floor')
        tower = Tower.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        bag = Bag.objects.get(char=char)
        challenge = TowerChallenge.objects.get(tower=tower, char=char)

        if int(floor) <= challenge.floor:
            return Response('Invalid floor!', status=400)
        
        challenge.floor = int(floor)
        money.money += int(floor)*500
        challenge.save()
        money.save()
        
        for i in range(int(floor)//10):
            item = getRandomItem_function('')
            addItemtoBag_function(bag, item)
        challenge_ser = TowerChallengeSerializer(challenge)
        return Response(challenge_ser.data, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def FightResult(request):
    exchange = request.data.get('exchange')
    char_id = request.data.get('char_id')
    result = request.data.get('result')

    char_1 = Characters.objects.get(user=request.user)
    char_2 = Characters.objects.get(id=char_id)
    bag_1 = Bag.objects.get(char=char_1)
    bag_2 = Bag.objects.get(char=char_2)
    money_1 = Money.objects.get(char=char_1)
    money_2 = Money.objects.get(char=char_2)

    if exchange == '0':
        if result == '1':
            return Response('Win', status=201)
        else:
            return Response('Lose', status=202)
    else:
        if result == '1':
            if random.randint(0, 5) != 1:
                rand_money = random.randint(0, 10000)
                if money_2.money - rand_money < 0:
                    money = money_2.money
                    money_1.money += money
                    money_2.money = 0
                    money_1.save()
                    money_2.save()
                    return Response({'money': money}, status=200)
                else:
                    money_2.money -= rand_money
                    money_1.money += rand_money
                    money_1.save()
                    money_2.save()
                    return Response({'money': rand_money}, status=200)
            else:
                bag_2_item = bag_2.items
                index = random.randint(0, len(bag_2_item))
                item_id = list(bag_2_item.keys())[index]
                item = Item.objects.get(id=item_id)
                addItemtoBag_function(bag_1, item)
                removeItemfromBag_function(bag_2, item)
                item_ser = ItemSerializer(item)
                return Response(item_ser.data, status=200)
        else:
            return Response('Lose', status=202)


@permission_classes([permissions.IsAuthenticated])
class ChallengeBoardView(APIView):
    def get(self, request, id):
        board = ChallengeBoard.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        try:
            my_rank = board.rank[str(char.id)]
        except:
            board.rank[str(char.id)] = 0
            board.save()
        board_ser = ChallengeBoardSerializer(board)
        return Response(board_ser.data, status=200)
    
    def post(self, request, id):
        char_id = request.data.get('char_id')
        board = ChallengeBoard.objects.get(id=id)
        char_1 = Characters.objects.get(user=request.user)
        char_2 = Characters.objects.get(id=char_id)

        rank_1 = board.rank[str(char_1.id)]
        rank_2 = board.rank[str(char_2.id)]
        if rank_2 > rank_1:
            board.rank[str(char_1.id)] = rank_2
            board.rank[str(char_2.id)] = rank_1
            board.save()
        
        result = {}
        result['id'] = str(char_1.id)
        result['name'] = char_1.name
        result['appearance'] = char_1.appearance.url
        result['rank'] = board.rank[str(char_1.id)]
        return Response(result, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getNearRankinBoard(request, id):
    board = ChallengeBoard.objects.get(id=id)
    char = Characters.objects.get(user=request.user)
    my_rank = board.rank[str(char.id)]

    results = []
    for key, value in board.rank.items():
        if value == my_rank + 1:
            this_char = Characters.objects.get(id=key)
            results.append({
                'id': str(this_char.id),
                'name': this_char.name,
                'appearance': this_char.appearance.url,
                'rank': value
            })
        elif value == my_rank - 1:
            this_char = Characters.objects.get(id=key)
            results.append({
                'id': str(this_char.id),
                'name': this_char.name,
                'appearance': this_char.appearance.url,
                'rank': value
            })
    return Response(results, status=200)
