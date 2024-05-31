from rest_framework import serializers
from .models import City, Tower, Question, QuestionChar, Arena
from app_user.models import Characters


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {'answer_correct': {'write_only': True}}


class QuestionCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChar
        fields = '__all__'


class ArenaSerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = Arena
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        char = Characters.objects.get(user=request.user)
        try:
            count = Arena.objects.latest('number').number + 1
        except:
            count = 1
        
        validated_data['char'] = char
        validated_data['number'] = count
        arena = Arena(**validated_data)
        arena.save()
        return arena

    def get_char(self, obj):
        return {
            "id": str(obj.char.id),
            "name": obj.char.name,
            "appearance": obj.char.appearance.url
        }