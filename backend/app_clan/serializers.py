from rest_framework import serializers

from .models import Clan, ClanPosition, RequestClan, OnlineClan
from app_user.models import Characters


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = '__all__'
    
    def create(self, validated_data):
        clan = Clan(**validated_data)
        clan.save()
        OnlineClan.objects.create(clan=clan)
        try:
            request = self.context.get('request')
            char = Characters.objects.get(user=request.user)
            ClanPosition.objects.create(char=char, clan=clan, position='1')
        except Exception as e:
            clan.delete()
            return serializers.ValidationError(str(e))
        return clan
    

class ClanPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClanPosition
        fields = '__all__'


class RequestClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestClan
        fields = '__all__'


class OnlineClanSerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = OnlineClan
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