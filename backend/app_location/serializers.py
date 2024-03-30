from rest_framework import serializers
from .models import City, Tower, Question, QuestionChar


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
        fields = ('id', 'number', 'question', 'answer_1', 'answer_2', 'answer_3')


class QuestionCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChar
        fields = '__all__'