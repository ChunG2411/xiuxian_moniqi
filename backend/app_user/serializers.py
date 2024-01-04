from rest_framework import serializers

from .models import User, Characters, Properties, Gifted, Bag, Equipped, Money, Knowledge, Study, Relationship
from app_item.models import Item, Book
from app_item.serializers import ItemSerializer, BookSerializer
from app_clan.models import ClanPosition
from app_clan.serializers import ClanPositionSerializer

class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        password = request.data.get('password')

        if len(password) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        
        password_split = [*password]
        if ord(password_split[0]) not in range(65, 90):
            raise serializers.ValidationError("The first letter of the password must be capitalized.")
        check_have_number = False
        for i in password_split:
            if ord(i) in range(48, 57):
                check_have_number = True
                break
        if not check_have_number:
            raise serializers.ValidationError("Password must contain number.")
        validated_data['password'] = password

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class CharactersSerializers(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    clan = serializers.SerializerMethodField()
    gifted = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Characters
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        name = request.data.get('name')
        gender = request.data.get('gender')
        background = request.data.get('background')

        char = Characters.objects.create(user=request.user, name=name, gender=gender, background=background)
        properties = Properties.objects.create(char=char)
        Bag.objects.create(char=char)
        Equipped.objects.create(char=char)
        Money.objects.create(char=char)
        Knowledge.objects.create(char=char)
        Study.objects.create(char=char)

        try:
            gifted_split = request.data.get('gifted_list').split(',')
            for i in gifted_split:
                gifted = Gifted.objects.get(id=int(i))
                char.gifted.add(gifted)
                properties_dict = dict(gifted.properties)
                for j in properties_dict:
                    old_value = getattr(properties, j)
                    setattr(properties, j, old_value + properties_dict[j])
                properties.save()
            char.save()  
        except:
            char.delete()
            return ""

        return char
    
    def get_properties(self, obj):
        property = Properties.objects.get(char=obj)
        pro_ser = PropertiesSerializer(property)
        return pro_ser.data

    def get_clan(self, obj):
        try:
            clan_position = ClanPosition.objects.get(char=obj)
            return ClanPositionSerializer(clan_position).data
        except: return None
    
    def get_gifted(self, obj):
        results = []
        for i in obj.gifted.all():
            results.append(i.name)
        return results
    
    def get_title(self, obj):
        results = []
        for i in obj.title.all():
            results.append(i.name)
        return results


class GiftedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gifted
        fields = '__all__'


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
            results.append(i.name)
        return results


class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Money
        fields = '__all__'
    

class EquippedSerializer(serializers.ModelSerializer):
    hand = serializers.SerializerMethodField()
    foot = serializers.SerializerMethodField()
    shirt = serializers.SerializerMethodField()
    trousers = serializers.SerializerMethodField()

    class Meta:
        model = Equipped
        fields = '__all__'

    def get_hand(self, obj):
        return ItemSerializer(obj.hand).data if obj.hand else ""

    def get_foot(self, obj):
        return ItemSerializer(obj.foot).data if obj.foot else ""

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


class RelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relationship
        fields = '__all__'