from rest_framework import serializers

from .models import (
    Clan, ClanPosition, RequestClan,
    Organization, OrganizationPosition
)
from app_user.models import Characters


class ClanSerializer(serializers.ModelSerializer):
    leader = serializers.SerializerMethodField()

    class Meta:
        model = Clan
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        char = Characters.objects.get(user=request.user)
        try:
            position = ClanPosition.objects.get(char=char)
            if position.position == 0:
                return serializers.ValidationError("You are leader of another clan")
            position.delete()
        except:
            pass

        validated_data['leader'] = char
        clan = Clan(**validated_data)
        clan.save()
        ClanPosition.objects.create(char=char, clan=clan, position=0)

        return clan

    def get_leader(self, obj):
        return {
            'id': str(obj.leader.id),
            'name': obj.leader.name
        }


class ClanPositionSerializer(serializers.ModelSerializer):
    clan = serializers.SerializerMethodField()
    char = serializers.SerializerMethodField()

    class Meta:
        model = ClanPosition
        fields = '__all__'

    def get_clan(self, obj):
        return ClanSerializer(obj.clan).data

    def get_char(self, obj):
        return {
            'id': str(obj.char.id),
            'name': obj.char.name,
            'appearance': obj.char.appearance.url
        }


class RequestClanSerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = RequestClan
        fields = '__all__'

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
            OrganizationPosition.objects.create(
                char=char, organization=organization, position=0)
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