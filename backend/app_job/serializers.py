from rest_framework import serializers

from .models import Seed,  Gardent, GardentSlot, StoreHouse, House, Mines
from app_item.serializers import ItemSerializer

class SeedSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Seed
        fields = '__all__'
    
    def get_item(self, obj):
        return ItemSerializer(obj.item).data if obj.item else None


class GardentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardent
        fields = '__all__'


class GardentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardentSlot
        fields = '__all__'


class StoreHouseSerializer(serializers.ModelSerializer):
    seed = serializers.SerializerMethodField()

    class Meta:
        model = StoreHouse
        fields = '__all__'

    def get_seed(self, obj):
        results = []
        for i in obj.seed:
            seed = Seed.objects.get(id=i)
            seed_ser = SeedSerializer(seed).data
            seed_ser['quantity'] = obj.seed[i]
            results.append(seed_ser)
        return results


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class MinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mines
        fields = '__all__'
        