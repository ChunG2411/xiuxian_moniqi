from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

from .models import (
    Seed, House, Oven,
    Gardent, GardentSlot,
    Cage, CageSlot,
    Lake, LakeSlot
)
from .serializers import (
    SeedSerializer, HouseSerializer, OvenSerializer,
    GardentSerializer, GardentSlotSerializer,
    CageSerializer, CageSlotSerializer,
    LakeSerializer, LakeSlotSerializer
)
from app_item.models import Item
from app_item.serializers import ItemSerializer
from app_user.models import Bag, Characters, Properties, Money
from xiuxian_moniqi.config import START_TIME
from xiuxian_moniqi.function import f_addItemtoBag, f_addSeedtoStore, f_removeSeedtoStore

from datetime import datetime, timedelta


# Create your views here.

@permission_classes([permissions.IsAuthenticated])
class HouseView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            house = House.objects.get(char=char)
            house_ser = HouseSerializer(house)
            return Response(house_ser.data, status=200)
        except:
            return Response("Don't have house.", status=400)

    def post(self, request):
        quality = request.data.get('quality')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        try:
            House.objects.get(char=char)
            return Response("House already exist!", status=400)
        except:
            money.money -= int(quality)*20000
            if money.money < 0:
                return Response("Don't enough money!", status=400)
            house = House.objects.create(char=char, quality=quality)
            money.save()
            house_ser = HouseSerializer(house)
            return Response(house_ser.data, status=200)

    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        House.objects.get(char=char).delete()
        return Response("Delete successful!", status=200)

    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        house = House.objects.get(char=char)
        house.name = name
        house.save()
        house_ser = HouseSerializer(house)
        return Response(house_ser.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class SeedView(APIView):
    def get(self, request):
        type = request.query_params.get('type')
        if not type:
            seeds = Seed.objects.all()
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(seeds, request)
            seed_ser = SeedSerializer(page, many=True)
            return pagination.get_paginated_response(seed_ser.data)
        else:
            seeds = Seed.objects.filter(type=type)
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(seeds, request)
            seed_ser = SeedSerializer(page, many=True)
            return pagination.get_paginated_response(seed_ser.data)

    def post(self, request):
        seed_ser = SeedSerializer(data=request.data)
        if seed_ser.is_valid():
            seed_ser.save()
            return Response(seed_ser.data, status=200)
        else:
            return Response(seed_ser.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
class SeedDetailView(APIView):
    def get(self, request, id):
        seed = Seed.objects.get(id=id)
        seed_ser = SeedSerializer(seed)
        return Response(seed_ser.data, status=200)

    def delete(self, request, id):
        Seed.objects.get(id=id).delete()
        return Response("Deleted successful.", status=200)


@permission_classes([permissions.IsAuthenticated])
class StoreView(APIView):
    def get(self, request, id):
        type = request.query_params.get('type')
        if type:
            char = Characters.objects.get(user=request.user)
            house = House.objects.get(char=char)
            store = HouseSerializer(house).data['store']
            return Response([i for i in store if i['type'] == type], status=200)
        else:
            char = Characters.objects.get(user=request.user)
            house = House.objects.get(char=char)
            store = HouseSerializer(house).data['store']
            return Response(store, status=200)

    def post(self, request, id):
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        house = House.objects.get(char=char)
        seed = Seed.objects.get(id=id)

        if money.money - seed.price < 0:
            return Response("Money not enough.", status=400)
        money.money -= seed.price
        money.save()
        f_addSeedtoStore(house, seed)
        return Response("Buy seed successful.", status=200)

    def delete(self, request, id):
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        house = House.objects.get(char=char)
        seed = Seed.objects.get(id=id)

        money.money += seed.price * 0.75
        money.save()
        f_removeSeedtoStore(house, seed)
        return Response("Sell seed successful.", status=200)


@permission_classes([permissions.IsAuthenticated])
class GardentView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            gardent = Gardent.objects.get(char=char)
            gar_ser = GardentSerializer(gardent)
            return Response(gar_ser.data, status=200)
        except:
            return Response("Don't have gardent", status=400)

    def post(self, request):
        quality = request.data.get('quality')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if money.money < int(quality)*10000:
            return Response("Don't enough money!", status=400)
        try:
            Gardent.objects.get(char=char)
            return Response("Gardent already exist!", status=400)
        except:
            gardent = Gardent.objects.create(char=char, quality=quality)
            money.money -= int(quality)*10000
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
        char = Characters.objects.get(user=request.user)
        Gardent.objects.get(char=char).delete()
        return Response("Delete gardent successful!", status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upgrateGardent(request):
    char = Characters.objects.get(user=request.user)
    gardent = Gardent.objects.get(char=char)
    if gardent.exp >= gardent.level * 100:
        gardent.exp -= gardent.level * 100
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
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(gardent_slot, request)
        gar_slot_ser = GardentSlotSerializer(page, many=True)
        return pagination.get_paginated_response(gar_slot_ser.data)

    def post(self, request):
        char = Characters.objects.get(user=request.user)
        gardent = Gardent.objects.get(char=char)
        money = Money.objects.get(char=char)
        slot = GardentSlot.objects.filter(gardent=gardent).count()

        if slot == gardent.quality * 10:
            return Response("The gardent slot limit has been reached!", status=400)

        money.money -= (slot + 1)*2000
        if money.money < 0:
            return Response("Don't enough money!", status=400)
        money.save()
        GardentSlot.objects.create(gardent=gardent)
        return Response("Buy new slot successful.", status=200)


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

        if slot.end_time <= timezone.now():
            f_addItemtoBag(bag, slot.seed.item)
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
        house = House.objects.get(char=char)

        if not slot.seed:
            slot.seed = seed
            slot.end_time = datetime.now(
                timezone.utc) + timedelta(minutes=int(seed.time))
            slot.save()
            f_removeSeedtoStore(house, seed)
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
class CageView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            cage = Cage.objects.get(char=char)
            cage_ser = CageSerializer(cage)
            return Response(cage_ser.data, status=200)
        except:
            return Response("Don't have cage", status=400)

    def post(self, request):
        quality = request.data.get('quality')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if money.money < int(quality)*10000:
            return Response("Don't enough money!", status=400)
        try:
            Cage.objects.get(char=char)
            return Response("Cage already exist!", status=400)
        except:
            cage = Cage.objects.create(char=char, quality=quality)
            money.money -= int(quality)*10000
            money.save()
            cage_ser = CageSerializer(cage)
            return Response(cage_ser.data, status=200)

    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        cage = Cage.objects.get(char=char)
        cage.name = name
        cage.save()
        cage_ser = CageSerializer(cage)
        return Response(cage_ser.data, status=200)

    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        Cage.objects.get(char=char).delete()
        return Response("Delete cage successful!", status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upgrateCage(request):
    char = Characters.objects.get(user=request.user)
    cage = Cage.objects.get(char=char)
    if cage.exp >= cage.level * 100:
        cage.exp -= cage.level * 100
        cage.level += 1
        cage.save()
        cage_ser = CageSerializer(cage)
        return Response(cage_ser.data, status=200)
    else:
        return Response("Cage don't enough exp", status=400)


@permission_classes([permissions.IsAuthenticated])
class CageSlotView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        cage = Cage.objects.get(char=char)
        cage_slot = GardentSlot.objects.filter(cage=cage)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(cage_slot, request)
        cage_slot_ser = CageSlotSerializer(page, many=True)
        return pagination.get_paginated_response(cage_slot_ser.data)

    def post(self, request):
        char = Characters.objects.get(user=request.user)
        cage = Cage.objects.get(char=char)
        money = Money.objects.get(char=char)
        slot = CageSlot.objects.filter(cage=cage).count()

        if slot == cage.quality * 10:
            return Response("The cage slot limit has been reached!", status=400)

        money.money -= (slot + 1)*2000
        if money.money < 0:
            return Response("Don't enough money!", status=400)
        money.save()
        CageSlot.objects.create(cage=cage)
        return Response("Buy new slot successful.", status=200)


@permission_classes([permissions.IsAuthenticated])
class SlaughterSeedView(APIView):
    def get(self, request, id):
        char = Characters.objects.get(user=request.user)
        bag = Bag.objects.get(char=char)
        cage = Cage.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        slot = CageSlot.objects.get(id=id)

        if not slot.seed:
            return Response("Don't have seed", status=400)

        if slot.end_time <= timezone.now():
            f_addItemtoBag(bag, slot.seed.item)
            slot.seed = None
            slot.end_time = None
            slot.save()
            cage.exp += 1
            cage.save()
            properties.duoc_lieu += 1
            properties.save()
            return Response(CageSlotSerializer(slot).data, status=200)
        else:
            return Response("It's not time yet!", status=400)

    def post(self, request, id):
        seed_id = request.data.get('seed_id')
        slot = CageSlot.objects.get(id=id)
        seed = Seed.objects.get(id=seed_id)
        char = Characters.objects.get(user=request.user)
        house = House.objects.get(char=char)

        if not slot.seed:
            slot.seed = seed
            slot.end_time = datetime.now(
                timezone.utc) + timedelta(minutes=int(seed.time))
            slot.save()
            f_removeSeedtoStore(house, seed)
            return Response(CageSlotSerializer(slot).data, status=200)
        else:
            return Response("Seed already exist!", status=400)

    def delete(self, request, id):
        try:
            slot = CageSlot.objects.get(id=id)
            slot.seed = None
            slot.end_time = None
            slot.save()
            slot_ser = CageSlotSerializer(slot)
            return Response(slot_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class LakeView(APIView):
    def get(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            lake = Lake.objects.get(char=char)
            lake_ser = LakeSerializer(lake)
            return Response(lake_ser.data, status=200)
        except:
            return Response("Don't have lake", status=400)

    def post(self, request):
        quality = request.data.get('quality')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)

        if money.money < int(quality)*10000:
            return Response("Don't enough money!", status=400)
        try:
            Lake.objects.get(char=char)
            return Response("Lake already exist!", status=400)
        except:
            lake = Lake.objects.create(char=char, quality=quality)
            money.money -= int(quality)*10000
            money.save()
            lake_ser = LakeSerializer(lake)
            return Response(lake_ser.data, status=200)

    def patch(self, request):
        name = request.data.get('name')
        char = Characters.objects.get(user=request.user)
        lake = Lake.objects.get(char=char)
        lake.name = name
        lake.save()
        lake_ser = LakeSerializer(lake)
        return Response(lake_ser.data, status=200)

    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        Lake.objects.get(char=char).delete()
        return Response("Delete lake successful!", status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upgrateLake(request):
    char = Characters.objects.get(user=request.user)
    lake = Lake.objects.get(char=char)
    if lake.exp >= lake.level * 100:
        lake.exp -= lake.level * 100
        lake.level += 1
        lake.save()
        lake_ser = LakeSerializer(lake)
        return Response(lake_ser.data, status=200)
    else:
        return Response("Lake don't enough exp", status=400)


@permission_classes([permissions.IsAuthenticated])
class LakeSlotView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        lake = Lake.objects.get(char=char)
        lake_slot = LakeSlot.objects.filter(lake=lake)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(lake_slot, request)
        lake_slot_ser = CageSlotSerializer(page, many=True)
        return pagination.get_paginated_response(lake_slot_ser.data)

    def post(self, request):
        char = Characters.objects.get(user=request.user)
        lake = Lake.objects.get(char=char)
        money = Money.objects.get(char=char)
        slot = LakeSlot.objects.filter(lake=lake).count()

        if slot == lake.quality * 10:
            return Response("The lake slot limit has been reached!", status=400)

        money.money -= (slot + 1)*2000
        if money.money < 0:
            return Response("Don't enough money!", status=400)
        money.save()
        LakeSlot.objects.create(lake=lake)
        return Response("Buy new slot successful.", status=200)


@permission_classes([permissions.IsAuthenticated])
class FishingSeedView(APIView):
    def get(self, request, id):
        char = Characters.objects.get(user=request.user)
        bag = Bag.objects.get(char=char)
        lake = Lake.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        slot = LakeSlot.objects.get(id=id)

        if not slot.seed:
            return Response("Don't have seed", status=400)

        if slot.end_time <= timezone.now():
            f_addItemtoBag(bag, slot.seed.item)
            slot.seed = None
            slot.end_time = None
            slot.save()
            lake.exp += 1
            lake.save()
            properties.duoc_lieu += 1
            properties.save()
            return Response(LakeSlotSerializer(slot).data, status=200)
        else:
            return Response("It's not time yet!", status=400)

    def post(self, request, id):
        seed_id = request.data.get('seed_id')
        slot = LakeSlot.objects.get(id=id)
        seed = Seed.objects.get(id=seed_id)
        char = Characters.objects.get(user=request.user)
        house = House.objects.get(char=char)

        if not slot.seed:
            slot.seed = seed
            slot.end_time = datetime.now(
                timezone.utc) + timedelta(minutes=int(seed.time))
            slot.save()
            f_removeSeedtoStore(house, seed)
            return Response(LakeSlotSerializer(slot).data, status=200)
        else:
            return Response("Seed already exist!", status=400)

    def delete(self, request, id):
        try:
            slot = LakeSlot.objects.get(id=id)
            slot.seed = None
            slot.end_time = None
            slot.save()
            slot_ser = LakeSlotSerializer(slot)
            return Response(slot_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@permission_classes([permissions.IsAuthenticated])
class OvenView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        try:
            oven = Oven.objects.get(char=char)
            serializer = OvenSerializer(oven)
            return Response(serializer.data, status=200)
        except:
            return Response("Don't have oven", status=400)
    
    def post(self, request):
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        try:
            Oven.objects.get(char=char)
            return Response("Oven already exist", status=400)
        except:
            money.money -= 100000
            if money.money < 0:
                return Response("Don't enough money", status=400)
            money.save()
            oven = Oven.objects.create(char=char)
            serializer = OvenSerializer(oven)
            return Response(serializer.data, status=200)
    
    def patch(self, request):
        char = Characters.objects.get(user=request.user)
        oven = Oven.objects.get(char=char)
        money = Money.objects.get(char=char)

        money.money -= (oven.level + 1) * 100000
        if money.money < 0:
            return Response("Don't enough money", status=400)
        money.save()
        oven.level += 1
        oven.save()
        serializer = OvenSerializer(oven)
        return Response(serializer.data, status=200)
    
    def delete(self, request):
        char = Characters.objects.get(user=request.user)
        Oven.objects.get(char=char).delete()
        return Response("Delete oven successful", status=200)


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
    start_time = datetime.strptime(
        START_TIME, "%d-%m-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
    duration = now - start_time

    return Response({
        "year": (duration.days * 288) // 365,
        "day": (duration.days * 288) % 365
    }, status=200)
