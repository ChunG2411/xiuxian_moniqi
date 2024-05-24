from rest_framework import serializers

from .models import (
    User, Characters, Properties, Title,
    Bag, Equipped, Money, Knowledge, Study, Relationship, StudyProcess,
    OwnPet
)
from app_item.models import Item, Book
from app_item.serializers import ItemSerializer, BookSerializer, PetSerializer, MenuSerializer
from app_clan.models import ClanPosition
from app_organization.models import Locality


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class CharactersSerializers(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    clan = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Characters
        fields = "__all__"

    def create(self, validated_data):
        char = Characters(**validated_data)
        char.save()
        Properties.objects.create(char=char)
        Bag.objects.create(char=char)
        Equipped.objects.create(char=char)
        Money.objects.create(char=char)
        Knowledge.objects.create(char=char)
        Study.objects.create(char=char)
        StudyProcess.objects.create(char=char)
        OwnPet.objects.create(char=char)

        return char

    def get_properties(self, obj):
        property = Properties.objects.get(char=obj)
        pro_ser = PropertiesSerializer(property)
        return pro_ser.data

    def get_clan(self, obj):
        try:
            clan_position = ClanPosition.objects.get(char=obj)
            return {
                'id': str(clan_position.clan.id),
                'name': clan_position.clan.name,
                'position': clan_position.position
            }
        except:
            return ''

    def get_organization(self, obj):
        try:
            locality = Locality.objects.get(char=obj)
            return {
                'id': str(locality.organization.id),
                'name': locality.organization.name
            }
        except:
            return ''

    def get_title(self, obj):
        results = []
        for i in obj.title.all():
            results.append(i.name)
        return results
    

class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'


class BagSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()

    class Meta:
        model = Bag
        fields = '__all__'

    def get_items(self, obj):
        items_list = []
        for i in obj.items:
            item = Item.objects.get(id=i)
            item_ser = ItemSerializer(item).data
            item_ser['quantity'] = obj.items[i]
            items_list.append(item_ser)
        return items_list

    def get_books(self, obj):
        books_list = []
        for i in obj.books:
            book = Book.objects.get(id=i)
            book_ser = BookSerializer(book).data
            book_ser['quantity'] = obj.books[i]
            books_list.append(book_ser)
        return books_list


class KnowledgeSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()

    class Meta:
        model = Knowledge
        fields = '__all__'

    def get_menu(self, obj):
        results = []
        for i in obj.menu.all():
            menu_ser = MenuSerializer(i)
            results.append(menu_ser.data)
        return results


class MoneySerializer(serializers.ModelSerializer):
    char = serializers.SerializerMethodField()

    class Meta:
        model = Money
        fields = '__all__'
    
    def get_char(self, obj):
        return {
            'id': str(obj.char.id),
            'name': obj.char.name,
            'appearance': obj.char.appearance.url
        }


class EquippedSerializer(serializers.ModelSerializer):
    hand = serializers.SerializerMethodField()
    head = serializers.SerializerMethodField()
    shirt = serializers.SerializerMethodField()
    trousers = serializers.SerializerMethodField()

    class Meta:
        model = Equipped
        fields = '__all__'

    def get_hand(self, obj):
        return ItemSerializer(obj.hand).data if obj.hand else ""

    def get_head(self, obj):
        return ItemSerializer(obj.head).data if obj.head else ""

    def get_shirt(self, obj):
        return ItemSerializer(obj.shirt).data if obj.shirt else ""

    def get_trousers(self, obj):
        return ItemSerializer(obj.trousers).data if obj.trousers else ""


class StudySerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = '__all__'

    def get_book(self, obj):
        results = []
        for i in obj.book.all():
            results.append(BookSerializer(i).data)
        return results


class StudyProcessSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = StudyProcess
        fields = '__all__'

    def get_book(self, obj):
        return BookSerializer(obj.book).data if obj.book else ""


class OwnPetSerializer(serializers.ModelSerializer):
    pet = serializers.SerializerMethodField()

    class Meta:
        model = OwnPet
        fields = '__all__'

    def get_pet(self, obj):
        return PetSerializer(obj.pet).data if obj.pet else ""
    

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'