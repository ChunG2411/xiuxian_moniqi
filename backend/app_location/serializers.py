from rest_framework import serializers
from .models import City, Tower


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class TowerSerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = Tower
        fields = '__all__'
    
    def get_char(self, obj):
        return {
            "id"    : str(obj.char.id),
            "name"  : obj.char.name,
            "appearance": obj.char.appearance.url
        }