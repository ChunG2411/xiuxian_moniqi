from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from .models import  Seed, Gardent, GardentSlot, StoreHouse, House, Mines
from .serializers import (
    SeedSerializer,
    GardentSerializer,
    StoreHouseSerializer,
    GardentSlotSerializer,
    HouseSerializer,
    MinesSerializer
)
from app_item.serializers import ItemSerializer
from app_item.views import addItemtoBag_function, getRandomItem_function
from app_user.models import Bag, Characters, Properties, Money
from xiuxian_moniqi.config import START_TIME

from datetime import datetime, timedelta, timezone

# Create your views here.

@permission_classes([permissions.IsAuthenticated])
class StoreHouseView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            storehouse = StoreHouse.objects.get(char=char)
            store_ser = StoreHouseSerializer(storehouse)
            return Response(store_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        storehouse = StoreHouse.objects.get(char=char)
        storehouse.name = name
        storehouse.save()
        store_ser = StoreHouseSerializer(storehouse)
        return Response(store_ser.data, status=200)
    
    def post(self, request):
        seed_id = request.data.get('seed_id')
        try:
            seed = Seed.objects.get(id=seed_id)
            char = Characters.objects.get(user=request.user)
            money = Money.objects.get(char=char)
            storehouse = StoreHouse.objects.get(char=char)

            try:
                storehouse.seed[str(seed.id)] += 1
            except:
                storehouse.seed[str(seed.id)] = 1
            money.money -= seed.price
            if money.money <= 0:
                return Response("Don't enough money!", status=400)
            storehouse.save()
            money.save()
            return Response("Add seed successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def delete(self, request):
        seed_id = request.query_params.get('seed_id')
        try:
            seed = Seed.objects.get(id=seed_id)
            char = Characters.objects.get(user=request.user)
            storehouse = StoreHouse.objects.get(char=char)
            try:
                storehouse.seed[str(seed.id)] -= 1
                if storehouse.seed[str(seed.id)] <= 0:
                    del storehouse.seed[str(seed.id)]
            except:
                del storehouse.seed[str(seed.id)]
            storehouse.save()
            return Response("Remove seed successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getSeed(request):
    seeds = Seed.objects.all()
    seed_ser = SeedSerializer(seeds, many=True)
    return Response(seed_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getSeedDetail(request, id):
    seed = Seed.objects.get(id=id)
    seed_ser = SeedSerializer(seed)
    return Response(seed_ser.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class GardentView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            gardent = Gardent.objects.get(char=char)
            gar_ser = GardentSerializer(gardent)
            return Response(gar_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def post(self, request):
        quality = request.data.get('quality')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if money.money <= int(quality)*1000:
            return Response("Don't enough money!", status=400)
        try:
            Gardent.objects.get(char=char)
            return Response("Gardent already exist!", status=400)
        except:
            gardent = Gardent.objects.create(char=char, quality=quality)
            StoreHouse.objects.create(char=char)
            money.money -= int(quality)*1000
            money.save()
            gar_ser = GardentSerializer(gardent)
            return Response(gar_ser.data, status=200)
    
    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        gardent = Gardent.objects.get(char=char)
        gardent.name = name
        gardent.save()
        gar_ser = GardentSerializer(gardent)
        return Response(gar_ser.data, status=200)

    def delete(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            Gardent.objects.get(char=char).delete()
            StoreHouse.objects.get(char=char).delete()
            return Response("Delete gardent successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upgrateGardent(request):
    char = Characters.objects.get(user=request.user)
    gardent = Gardent.objects.get(char=char)
    if gardent.exp >= 100:
        gardent.exp -= 100
        gardent.level += 1
        gardent.save()
        gar_ser = GardentSerializer(gardent)
        return Response(gar_ser.data, status=200)
    else:
        return Response("Gardent don't enough exp", status=400)
    

@permission_classes([permissions.IsAuthenticated])
class GardentSlotView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        gardent = Gardent.objects.get(char=char)
        gardent_slot = GardentSlot.objects.filter(gardent=gardent)
        gar_slot_ser = GardentSlotSerializer(gardent_slot, many=True)
        return Response(gar_slot_ser.data, status=200)
    
    def post(self, request):
        price = request.data.get('price')
        char = Characters.objects.get(user=request.user)
        gardent = Gardent.objects.get(char=char)
        money = Money.objects.get(char=char)
        slot = GardentSlot.objects.filter(gardent=gardent)

        if slot == gardent.quality * 10:
            return Response("The gardent slot limit has been reached!", status=400)

        money.money -= int(price)
        if money.money < 0:
            return Response("Don't enough money!", status=400)
        money.save()
        gardent_slot = GardentSlot.objects.create(gardent=gardent)
        gar_slot_ser = GardentSlotSerializer(gardent_slot)
        return Response(gar_slot_ser.data, status=200)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upgradeSlot(request, id):
    char = Characters.objects.get(user=request.user)
    money = Money.objects.get(char=char)
    
    gardent_slot = GardentSlot.objects.get(id=id)
    if gardent_slot.level == 9:
        return Response("Gardent slot level is max!", status=400)

    gardent_slot.level += 1
    money.money -= gardent_slot.level * 1000
    if money.money < 0:
        return Response("Don't enough money!", status=400)
    gardent_slot.save()
    money.save()
    
    gar_slot_ser = GardentSlotSerializer(gardent_slot)
    return Response(gar_slot_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getNextSlotPrice(request):
    char = Characters.objects.get(user=request.user)
    gardent = Gardent.objects.get(char=char)
    gardent_slot = GardentSlot.objects.filter(gardent=gardent)
    slot_length = len(gardent_slot)
    return Response(str((slot_length+1)*1000), status=200)


@permission_classes([permissions.IsAuthenticated])
class HarvestSeedView(APIView):
    def get(self, request, id):
        char = Characters.objects.get(user=request.user)
        bag = Bag.objects.get(char=char)
        gardent = Gardent.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        slot = GardentSlot.objects.get(id=id)
        if not slot.seed:
            return Response("Don't have seed", status=400)
        
        if slot.end_time <= datetime.now(timezone.utc):
            addItemtoBag_function(bag, slot.seed.item)
            slot.seed = None
            slot.end_time = None
            slot.save()
            gardent.exp += 1
            gardent.save()
            properties.duoc_lieu += 1
            properties.save()
            return Response(GardentSlotSerializer(slot).data, status=200)
        else:
            return Response("It's not time yet!", status=400)


    def post(self, request, id):
        seed_id = request.data.get('seed_id')
        slot = GardentSlot.objects.get(id=id)
        seed = Seed.objects.get(id=seed_id)
        char = Characters.objects.get(user=request.user)
        storehouse = StoreHouse.objects.get(char=char)
        
        if not slot.seed:
            slot.seed = seed
            time = slot.seed.time * (10-slot.level)/10
            hours = int(time)
            minutes = (time - hours)*60
            slot.end_time = datetime.now(timezone.utc) + timedelta(hours=hours, minutes=minutes)
            slot.save()

            storehouse.seed[str(seed.id)] -= 1
            if storehouse.seed[str(seed.id)] <= 0:
                del storehouse.seed[str(seed.id)]
            storehouse.save()
            return Response(GardentSlotSerializer(slot).data, status=200)
        else:
            return Response("Seed already exist!", status=400)


    def delete(self, request, id):
        try:
            slot = GardentSlot.objects.get(id=id)
            slot.seed = None
            slot.end_time = None
            slot.save()
            slot_ser = GardentSlotSerializer(slot)
            return Response(slot_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@permission_classes([permissions.IsAuthenticated])
class HouseView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            house = House.objects.get(char=char)
            house_ser = HouseSerializer(house)
            return Response(house_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
        
    def post(self, request):
        quality = request.data.get('quality')
        change_gardent = request.data.get('change_gardent')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        try:
            House.objects.get(char=char)
            return Response("House already exist!", status=400)
        except:
            money.money -= int(quality)*10000
            if money.money < 0:
                return Response("Don't enough money!", status=400)
            house = House.objects.create(char=char, quality=quality)
            try:
                gardent = Gardent.objects.get(char=char)
                if not change_gardent:
                    house.delete()
                    return Response("You had gardent", status=400)
                if change_gardent == '1':
                    gardent.level = 1
                    gardent.exp = 0
                    gardent.quality = house.quality
                    gardent.save()
            except:
                Gardent.objects.create(char=char, quality=quality)
                StoreHouse.objects.create(char=char)
            money.save()
            house_ser = HouseSerializer(house)
            return Response(house_ser.data, status=200)
                
    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        try:
            House.objects.get(char=char).delete()
            Gardent.objects.get(char=char).delete()
            StoreHouse.objects.get(char=char).delete()
            return Response("Delete successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        
    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        house = House.objects.get(char=char)
        house.name = name
        house.save()
        house_ser = HouseSerializer(house)
        return Response(house_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMines(request):
    mines = Mines.objects.all()
    mines_ser = MinesSerializer(mines, many=True)
    return Response(mines_ser.data, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def getResultMines(request):
    time = request.data.get('time')
    mines_id = request.data.get('mines_id')

    char = Characters.objects.get(user=request.user)
    money = Money.objects.get(char=char)
    bag = Bag.objects.get(char=char)
    properties = Properties.objects.get(char=char)
    mines = Mines.objects.get(id=mines_id)
    
    item_quantity = int(int(time)/300)
    rise_money = int(mines.quantity*int(time)/60)
    item_got = []
    for i in range(item_quantity):
        item = getRandomItem_function(type='7')
        item_ser = ItemSerializer(item)
        item_got.append(item_ser.data)
        addItemtoBag_function(bag, item)
    money.money += rise_money
    money.save()
    properties.khoang_san += item_quantity
    properties.save()

    return Response({
        "money": rise_money,
        'item': item_got
    }, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def Meditation(request):
    quality = request.data.get('quality')
    time = request.data.get('time')
    time_final = int(time)*(1+int(quality)/10)

    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    properties.linh_luc += int(time_final/10)
    if properties.linh_luc > properties.linh_luc_yeu_cau:
        properties.linh_luc = properties.linh_luc_yeu_cau
    properties.save()
    return Response({
        'linh_luc': int(time_final/10)
    }, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getCurTime(request):
    now = datetime.now(timezone.utc)
    start_time = datetime.strptime(START_TIME, "%d-%m-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
    duration = now - start_time
    
    return Response({
        "year": (duration.days * 288) // 365,
        "day": (duration.days * 288) % 365
    }, status=200)

