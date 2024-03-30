from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Item, Menu, Book
from .serializers import ItemSerializer, MenuSerializer, BookSerializer
from app_user.models import Bag, Characters, Properties, Equipped
from app_job.models import Oven
from xiuxian_moniqi.function import f_addBooktoBag, f_getRandomBook, f_remove_properties, f_removeBookfromBag, f_removeItemfromBag, f_addItemtoBag, f_getRandomItem, f_getListItem, f_getListBook

import random


# Create your views here.

@permission_classes([permissions.IsAuthenticated])
class ItemView(APIView):
    def get(self, request):
        type = request.query_params.get('type')
        level = request.query_params.get('level')
        quality = request.query_params.get('quality')
        order_price = request.query_params.get('order_price')

        items = f_getListItem(type, quality, level, order_price)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(items, request)
        item_ser = ItemSerializer(page, many=True)
        return pagination.get_paginated_response(item_ser.data)
    
    def post(self, request):
        item_ser = ItemSerializer(data=request.data)
        if item_ser.is_valid():
            item_ser.save()
            return Response(item_ser.data, status=200)
        else:
            return Response(item_ser.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
class ItemDetailView(APIView):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            item_ser = ItemSerializer(item)
            return Response(item_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def delete(self, request, id):
        try:
            item = Item.objects.get(id=id)
            item.delete()
            return Response("Delete successful.", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getRandomItem(request):
    type = request.query_params.get('type')
    item = f_getRandomItem(type)
    item_ser = ItemSerializer(item)
    return Response(item_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def addItemtoBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        f_addItemtoBag(bag, item)
        return Response("Add item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def removeItemfromBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        equip = Equipped.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        bag = Bag.objects.get(char=char)

        if equip.head == item:
            f_remove_properties(properties, equip.head)
            equip.head = None
        elif equip.hand == item:
            f_remove_properties(properties, equip.hand)
            equip.hand = None
        elif equip.shirt == item:
            f_remove_properties(properties, equip.shirt)
            equip.shirt = None
        elif equip.trousers == item:
            f_remove_properties(properties, equip.trousers)
            equip.trousers = None
        equip.save()
        f_removeItemfromBag(bag, item)
        return Response("Remove item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class BookView(APIView):
    def get(self, request):
        level = request.query_params.get('level')
        attribute = request.query_params.get('attribute')
        quality = request.query_params.get('quality')
        order_price = request.query_params.get('order_price')

        books = f_getListBook(attribute, quality, level, order_price)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(books, request)
        book_ser = BookSerializer(page, many=True)
        return pagination.get_paginated_response(book_ser.data)

    def post(self, request):
        book_ser = BookSerializer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data, status=200)
        else:
            return Response(book_ser.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
class BookDetailView(APIView):
    def get(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book_ser = BookSerializer(book)
            return Response(book_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return Response("Delete successful.", status=200)
        except Exception as e:
            return Response(str(e), status=400)
        

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getRandomBook(request):
    type = request.query_params.get('type')
    book = f_getRandomBook(type)
    book_ser = BookSerializer(book)
    return Response(book_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def addBooktoBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        book = Book.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        f_addBooktoBag(bag, book)
        return Response("Add book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def removeBookfromBag(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        book = Book.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        f_removeBookfromBag(bag, book)
        return Response("Remove book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)
    

@permission_classes([permissions.IsAuthenticated])
class MenuView(APIView):
    def get(self, request):
        try:
            type = request.query_params.get('type')
            menu = Menu.objects.filter(type=type)
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(menu, request)
            menu_ser = MenuSerializer(page, many=True)
            return pagination.get_paginated_response(menu_ser.data)
        except Exception as e:
            return Response(str(e), status=400)
    
    def post(self, request):
        menu = MenuSerializer(context={"request": request}, data=request.data)
        if menu.is_valid():
            menu.save()
            return Response(menu.data, status=200)
        else:
            return Response(menu.errors, status=400)


@permission_classes([permissions.IsAuthenticated])
class MenuDetailView(APIView):
    def get(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
            menu_ser = MenuSerializer(menu)
            return Response(menu_ser.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def delete(self, request, id):
        try:
            menu = Menu.objects.get(id=id)
            menu.delete()
            return Response("Delete successful.", status=200)
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
        oven = Oven.objects.get(char=char)

        mater_rate = 0
        char_rate = properties.may_man + properties.duoc_lieu + oven.level * 10
        final_rate = 0

        if menu.type == '1':
            char_rate += properties.luyen_khi
        elif menu.type == '2':
            char_rate += properties.luyen_dan
        
        if lucky_id:
            lucky_item = Item.objects.get(id=lucky_id)
            if lucky_item.type == '10':
                char_rate += lucky_item.properties['may_man']

        for i in mater_split:
            for j in menu.materials.all():
                if i == str(j.id):
                    mater_rate += (1/menu.materials.count())*500
        
        if char_rate >= 1000: char_rate = 1000
        if mater_rate >= 1000: mater_rate = 1000
        final_rate = (char_rate + mater_rate)/2

        if random.randint(0, 1000) <= final_rate:
            if lucky_id: f_removeItemfromBag(bag, lucky_item)
            for i in mater_split:
                try:
                    item = Item.objects.get(id=i)
                    f_removeItemfromBag(bag, item)
                except:
                    continue
            f_addItemtoBag(bag, menu.item)
            if menu.type == '1':
                properties.luyen_khi += 1
            elif menu.type == '2':
                properties.luyen_dan += 1
            properties.save()
            return Response("Create item successful!", status=200)
        else:
            if lucky_id: f_removeItemfromBag(bag, lucky_item)
            for i in mater_split:
                try:
                    item = Item.objects.get(id=i)
                    f_removeItemfromBag(bag, item)
                except Exception as e:
                    continue
            return Response("Create item fail!", status=400)
        
    except Exception as e:
        return Response(str(e), status=400)
