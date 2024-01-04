from rest_framework import serializers

from .models import Item, Menu, Book

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_item(self, obj):
        return ItemSerializer(obj.item).data
    
    def get_materials(self, obj):
        results = []
        for i in obj.materials.all():
            results.append(ItemSerializer(i).data)
        return results


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'