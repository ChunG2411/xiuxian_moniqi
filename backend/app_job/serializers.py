from rest_framework import serializers
from django.utils import timezone

from .models import (
        Seed, House, Oven,
        Gardent, GardentSlot, Cage, CageSlot, Lake, LakeSlot,
    )
from app_item.serializers import ItemSerializer


class SeedSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Seed
        fields = '__all__'
    
    def get_item(self, obj):
        return ItemSerializer(obj.item).data if obj.item else ""
    

class HouseSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = '__all__'

    def get_store(self, obj):
        results = []
        for i in obj.store:
            seed = Seed.objects.get(id=i)
            seed_ser = {
                'id'    : str(seed.id),
                'name'  : seed.name,
                'image' : seed.image.url,
                'type'  : seed.type,
                'quantity': obj.store[i]
            }
            results.append(seed_ser)
        return results


class GardentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardent
        fields = '__all__'


class GardentSlotSerializer(serializers.ModelSerializer):
    seed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = GardentSlot
        fields = '__all__'
    
    def get_seed(self, obj):
        return {
            "id": str(obj.seed.id),
            "name": obj.seed.name,
            "type": obj.seed.type,
            "image": obj.seed.image.url
        } if obj.seed else ""
    
    def get_status(self, obj):
        if not obj.seed:
            return '0'
        elif timezone.now() >= obj.end_time:
            return '1'
        else: return int((obj.end_time - timezone.now()).total_seconds())


class CageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cage
        fields = '__all__'


class CageSlotSerializer(serializers.ModelSerializer):
    seed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CageSlot
        fields = '__all__'
    
    def get_seed(self, obj):
        return {
            "id": str(obj.seed.id),
            "name": obj.seed.name,
            "type": obj.seed.type,
            "image": obj.seed.image.url
        } if obj.seed else ""
    
    def get_status(self, obj):
        if not obj.seed:
            return '0'
        elif timezone.now() >= obj.end_time:
            return '1'
        else: return (obj.end_time - timezone.now()).total_seconds()


class LakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lake
        fields = '__all__'


class LakeSlotSerializer(serializers.ModelSerializer):
    seed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = LakeSlot
        fields = '__all__'
    
    def get_seed(self, obj):
        return {
            "id": str(obj.seed.id),
            "name": obj.seed.name,
            "type": obj.seed.type,
            "image": obj.seed.image.url
        } if obj.seed else ""
    
    def get_status(self, obj):
        if not obj.seed:
            return '0'
        elif timezone.now() >= obj.end_time:
            return '1'
        else: return (obj.end_time - timezone.now()).total_seconds()


class OvenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oven
        fields = '__all__'
