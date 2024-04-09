from rest_framework import serializers

from .models import Item, Menu, Book, Pet

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

    def create(self, validated_data):
        request = self.context.get('request')
        item_id = request.data.get('item')

        validated_data['item'] = Item.objects.get(id=item_id)
        menu = Menu(**validated_data)
        menu.save()
        return menu
    
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


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'