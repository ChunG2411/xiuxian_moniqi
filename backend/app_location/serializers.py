from rest_framework import serializers

from .models import City, OnlineCity, Tower, TowerChallenge, ChallengeBoard
from app_user.models import Characters


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class OnlineCitySerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = OnlineCity
        fields = '__all__'
    
    def get_char(self, obj):
        results = []
        for i in obj.char.all():
            results.append({
                'id': str(i.id),
                'name': i.name,
                'appearance': i.appearance.url
            })
        return results


class TowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tower
        fields = '__all__'


class TowerChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TowerChallenge
        fields = '__all__'


class ChallengeBoardSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeBoard
        fields = '__all__'

    def get_rank(self, obj):
        results = []
        for i in obj.rank:
            result = {}
            char = Characters.objects.get(id=i)
            result['id'] = str(char.id)
            result['name'] = char.name
            result['appearance'] = char.appearance.url
            result['rank'] = obj.rank[i]
            results.append(result)
        return results

