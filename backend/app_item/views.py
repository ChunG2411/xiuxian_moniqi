from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from .models import Item, Menu, Book
from .serializers import ItemSerializer, MenuSerializer, BookSerializer
from app_user.models import Bag, Characters, Properties

import random

# Create your views here.
def removeItemfromBag_function(bag, item):
    try:
        bag.items[str(item.id)] -= 1
        if bag.items[str(item.id)] <= 0:
            del bag.items[str(item.id)]
    except:
        del bag.items[str(item.id)]
    bag.save()

def addItemtoBag_function(bag, item):
    try:
        bag.items[str(item.id)] += 1
    except:
        bag.items[str(item.id)] = 1
    bag.save()

def addBooktoBag_function(bag, item):
    try:
        bag.books[str(item.id)] += 1
    except:
        bag.books[str(item.id)] = 1
    bag.save()

def removeBookfromBag_function(bag, item):
    try:
        bag.books[str(item.id)] -= 1
        if bag.books[str(item.id)] <= 0:
            del bag.books[str(item.id)]
    except:
        del bag.books[str(item.id)]
    bag.save()


@permission_classes([permissions.IsAuthenticated])
class ItemView(APIView):
    def get(self, request):
        type = request.query_params.get('type')
        level = request.query_params.get('level')
        
        if not level:
            return Response("Level is required!", status=400)
        if type:
            items = Item.objects.filter(type=type, level__lte=level)
        else:
            items = Item.objects.filter(level__lte=level)

        item_ser = ItemSerializer(items, many=True)
        return Response(item_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ItemDetailView(request, id):
    try:
        item = Item.objects.get(id=id)
        item_ser = ItemSerializer(item)
        return Response(item_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

def getRandomItem_function(type):
    number = random.randint(0, 2048)
    if number == 1:
        quality = 10
    elif 1 < number <= 4:
        quality = 9
    elif 4 < number <= 9:
        quality = 8
    elif 9 < number <= 19:
        quality = 7
    elif 19 < number <= 50:
        quality = 6
    elif 50 < number <= 100:
        quality = 5
    elif 100 < number <= 200:
        quality = 4
    elif 200 < number <= 500:
        quality = 3
    elif 500 < number <= 1000:
        quality = 2
    else:
        quality = 1

    if not type:
        item = Item.objects.filter(quality=quality).order_by('?')[0]
    else:
        item = Item.objects.filter(type=type, quality=quality).order_by('?')[0]
    return item


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getRandomItem(request):
    type = request.query_params.get('type')
    item = getRandomItem_function(type)
    item_ser = ItemSerializer(item)
    return Response(item_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def addItemtoBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        try:
            bag.items[str(item.id)] += 1
        except:
            bag.items[str(item.id)] = 1
        bag.save()
        return Response("Add item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def removeItemfromBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        try:
            bag.items[str(item.id)] -= 1
            if bag.items[str(item.id)] <= 0:
                del bag.items[str(item.id)]
        except:
            del bag.items[str(item.id)]
        bag.save()
        return Response("Remove item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def removeBookfromBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        book = Book.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        try:
            bag.books[str(book.id)] -= 1
            if bag.books[str(book.id)] <= 0:
                del bag.books[str(book.id)]
        except:
            del bag.books[str(book.id)]
        bag.save()
        return Response("Remove book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMenu(request, id):
    try:
        menu = Menu.objects.get(id=id)
        menu_ser = MenuSerializer(menu)
        return Response(menu_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createItem(request):
    menu_id = request.data.get('menu_id')
    materials = request.data.get('materials')
    mater_split = materials.split(',')
    lucky_id = request.data.get('lucky_id')

    try:
        menu = Menu.objects.get(id=menu_id)
        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)
        bag = Bag.objects.get(char=char)

        mater_rate = 0
        char_rate = properties.may_man
        final_rate = 0

        if menu.type == '1':
            char_rate += properties.luyen_khi
        elif menu.type == '2':
            char_rate += properties.luyen_dan
        elif menu.type == '3':
            char_rate += properties.hoa_phu
        
        if lucky_id:
            lucky_item = Item.objects.get(id=lucky_id)
            if lucky_item.type == '8':
                char_rate += 300

        for i in mater_split:
            for j in menu.materials.all():
                if i == str(j.id):
                    mater_rate += (1/menu.materials.count())*500
        
        if char_rate >= 1000: char_rate = 1000
        if mater_rate >= 1000: mater_rate = 1000
        final_rate = (char_rate + mater_rate)/2

        if random.randint(0, 100) <= final_rate:
            if lucky_id: removeItemfromBag_function(bag, lucky_item)
            for i in mater_split:
                item = Item.objects.get(id=i)
                removeItemfromBag_function(bag, item)
            addItemtoBag_function(bag, menu.item)
            if menu.type == '1':
                properties.luyen_khi += 1
            elif menu.type == '2':
                properties.luyen_dan += 1
            elif menu.type == '3':
                properties.hoa_phu += 1
            return Response("Create item successful!", status=200)
        else:
            if lucky_id: removeItemfromBag_function(bag, lucky_item)
            for i in mater_split:
                item = Item.objects.get(id=i)
                removeItemfromBag_function(bag, item)
            return Response("Create item fail!", status=200)
        
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBook(request):
    level = request.query_params.get('level')
    attribute = request.query_params.get('attribute')
    
    if not level:
        return Response("Level is required!", status=400)
    if attribute:
        book = Book.objects.filter(level__lte=level, attribute=attribute)
    else:
        book = Book.objects.filter(level__lte=level)
    
    book_ser = BookSerializer(book, many=True)
    return Response(book_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBookDetail(request, id):
    try:
        book = Book.objects.get(id=id)
        book_ser = BookSerializer(book)
        return Response(book_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)