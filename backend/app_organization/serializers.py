from rest_framework import serializers
from django.utils import timezone

from .models import Organization, Locality, Mine, Market, Mail
from app_user.models import Characters

import random
from datetime import datetime


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class LocalitySerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    char = serializers.SerializerMethodField()

    class Meta:
        model = Locality
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        char = Characters.objects.get(user=request.user)

        validated_data['char'] = char
        validated_data['pos_x'] = random.randint(0, 1000)
        validated_data['pos_y'] = random.randint(0, 1000)
        locality = Locality(**validated_data)
        if not locality.name:
            locality.name = char.name
        locality.save()
        return locality
    
    def get_organization(self, obj):
        return {
            'id': str(obj.organization.id),
            'name': obj.organization.name
        } if obj.organization else ''
    
    def get_char(self, obj):
        return {
            'id': str(obj.char.id),
            'name': obj.char.name,
            'appearance': obj.char.appearance.url
        }


class MineSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()

    class Meta:
        model = Mine
        fields = '__all__'

    def create(self, validated_data):
        validated_data['pos_x'] = random.randint(0, 1000)
        validated_data['pos_y'] = random.randint(0, 1000)
        mine = Mine(**validated_data)
        mine.get_at = datetime.now(timezone.get_current_timezone())
        mine.save()
        return mine
    
    def get_owner(self, obj):
        return {
            'id': str(obj.owner.id),
            'name': obj.owner.name
        } if obj.owner else ''

    def get_store(self, obj):
        if obj.owner:
            now = datetime.now(timezone.get_current_timezone())
            duration = int((now - obj.get_at).total_seconds() / 60)
            store = obj.produce * duration
            if store >= obj.limit:
                store = obj.limit
            obj.store = store
            obj.save()
            return store
        else:
            return 0


class MarketSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = '__all__'

    def create(self, validated_data):
        validated_data['pos_x'] = random.randint(0, 1000)
        validated_data['pos_y'] = random.randint(0, 1000)
        market = Market(**validated_data)
        market.get_at = datetime.now(timezone.get_current_timezone())
        market.save()
        return market
    
    def get_owner(self, obj):
        return {
            'id': str(obj.owner.id),
            'name': obj.owner.name
        } if obj.owner else ''

    def get_store(self, obj):
        if obj.owner:
            now = datetime.now(timezone.get_current_timezone())
            duration = int((now - obj.get_at).total_seconds() / 60)
            store = obj.produce * duration
            if store >= obj.limit:
                store = obj.limit
            obj.store = store
            obj.save()
            return store
        else:
            return 0


class MailSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Mail
        fields = '__all__'
    
    def get_sender(self, obj):
        return {
            'id': str(obj.sender.id),
            'name': obj.sender.name,
            'organization': obj.sender.organization.name if obj.sender.organization else ''
        }
    
    def get_receiver(self, obj):
        return {
            'id': str(obj.receiver.id),
            'name': obj.receiver.name,
            'organization': obj.receiver.organization.name if obj.receiver.organization else ''
        }