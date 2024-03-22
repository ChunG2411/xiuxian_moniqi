from rest_framework import serializers

from .models import (
        Clan, ClanPosition, RequestClan,
        Organization, OrganizationPosition
    )
from app_user.models import Characters


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        clan = Clan(**validated_data)
        clan.save()
        try:
            char = Characters.objects.get(user=request.user)
            ClanPosition.objects.create(char=char, clan=clan, position=0)
        except Exception as e:
            clan.delete()
            return serializers.ValidationError(str(e))
        return clan
    

class ClanPositionSerializer(serializers.ModelSerializer):
    clan = serializers.SerializerMethodField()

    class Meta:
        model = ClanPosition
        fields = '__all__'
    
    def get_clan(self, obj):
        return ClanSerializer(obj.clan).data


class RequestClanSerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()
    clan = serializers.SerializerMethodField()

    class Meta:
        model = RequestClan
        fields = '__all__'
    
    def get_clan(self, obj):
        return ClanSerializer(obj.clan).data
    
    def get_char(self, obj):
        return {
            'id': str(obj.char.id),
            'name': obj.char.name,
            'appearance': obj.char.appearance.url
        }


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        organization = Organization(**validated_data)
        organization.save()
        try:
            char = Characters.objects.get(user=request.user)
            OrganizationPosition.objects.create(char=char, organization=organization, position=0)
        except Exception as e:
            organization.delete()
            return serializers.ValidationError(str(e))
        return organization
    

class OrganizationPositionSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationPosition
        fields = '__all__'

    def get_organization(self, obj):
        return OrganizationSerializer(obj.organization).data