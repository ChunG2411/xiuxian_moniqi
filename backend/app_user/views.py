from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.core.validators import validate_email

from .models import (
    User, Characters, Properties,
    Bag, Equipped, Money, Knowledge,
    Study, StudyProcess,
    Relationship
)
from .serializers import (
    UserRegisterSerializers, CharactersSerializers,
    BagSerializer, MoneySerializer, EquippedSerializer, KnowledgeSerializer,
    StudySerializer, StudyProcessSerializer,
    RelationshipSerializer
)
from app_item.models import Item, Menu, Book
from app_location.models import Tower
from app_location.serializers import TowerSerializer
from xiuxian_moniqi.function import f_add_properties, f_addBooktoBag, f_addItemtoBag, f_remove_properties, f_removeBookfromBag, f_removeItemfromBag

import random


# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            User.objects.get(email=email)
            return Response("Email already exist", status=400)
        except:
            try:
                validate_email(email)
            except:
                return Response("Email isn't valid", status=400)

        if len(password) < 6:
            return Response("Password must be at least 6 characters.", status=400)
        
        password_split = [*password]
        if ord(password_split[0]) not in range(65, 90):
            return Response("The first letter of the password must be capitalized.", status=400)
        
        check_have_number = False
        for i in password_split:
            if ord(i) in range(48, 57):
                check_have_number = True
                break
        if not check_have_number:
            return Response("Password must contain number.", status=400)

        serializer = UserRegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        username_email = request.data.get('username_email')
        password = request.data.get('password')

        user = None
        try:
            user = User.objects.get(username=username_email)
            username = username_email
        except:
            try:
                user = User.objects.get(email=username_email)
                username = user.username
            except:
                return Response("Username or Email don't exist.", status=400)

        if not user.check_password(password):
            return Response("Password incorect.", status=400)

        refresh = TokenObtainPairSerializer.get_token(user)
        user.last_login = timezone.now()
        user.save()
        response = {
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(response, status=200)


@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(Response("All refresh tokens blacklisted."), status=200)
        refresh_token = self.request.data.get('refresh_token')
        try:
            token = RefreshToken(token=refresh_token)
            token.blacklist()
        except:
            return Response("Token is blacklisted.", status=400)
        return Response("Logout successful.", status=200)


@permission_classes([permissions.IsAuthenticated])
class CharactersView(APIView):
    def get(self, request, id):
        try:
            char = Characters.objects.get(id=id)
            char_serializer = CharactersSerializers(char)
            return Response(char_serializer.data, status=200)
        except Exception as e:
            return Response(str(e), status=400)

    def post(self, request):
        request_copy = request.data.copy()
        request_copy['user'] = request.user.id
        try:
            Characters.objects.get(user=request.user)
            return Response("Character already exist!", status=400)
        except:
            char_serializer = CharactersSerializers(
                context={"request": request}, data=request_copy)
            if char_serializer.is_valid():
                char_serializer.save()
                return Response(char_serializer.data, status=200)
        return Response(char_serializer.errors, status=400)

    def delete(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            char.delete()
            return Response("Delete successfull!", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getCurrChar(request):
    try:
        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)
        duration = timezone.now() - char.date_join
        time = (duration.days * 288) // 365
        properties.tuoi = time + 1
        properties.save()

        if properties.tuoi > properties.tuoi_tho:
            return Response("The lifespan limit has been reached.", status=201)

        char_ser = CharactersSerializers(char)
        return Response(char_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBag(request):
    tab = request.query_params.get('tab')
    type = request.query_params.get('type')
    quality = request.query_params.get('quality')
    level = request.query_params.get('level')
    attribute = request.query_params.get('attribute')

    char = Characters.objects.get(user=request.user)
    bag = Bag.objects.get(char=char)
    bag_ser = BagSerializer(bag).data

    results = []
    if tab == '1':
        results = bag_ser["items"]
    else:
        results = bag_ser["books"]
    if type and tab == '1':
        results = [i for i in results if i["type"] == type]
    if attribute and tab == '2':
        results = [i for i in results if i["attribute"] == attribute]
    if quality:
        results = [i for i in results if i["quality"] == int(quality)]
    if level:
        results = [i for i in results if i["level"] == int(level)]

    return Response(results, status=200)


@permission_classes([permissions.IsAuthenticated])
class MoneyView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        money_ser = MoneySerializer(money)
        return Response(money_ser.data, status=200)

    def post(self, request):
        rise = request.data.get('rise')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        money.money += int(rise)
        money.save()
        money_ser = MoneySerializer(money)
        return Response(money_ser.data, status=200)

    def delete(self, request):
        decrease = request.query_params.get('decrease')
        char = Characters.objects.get(user=request.user)
        money = Money.objects.get(char=char)
        money.money -= int(decrease)
        if money.money <= 0:
            return Response("Don't enough money!", status=400)
        money.save()
        money_ser = MoneySerializer(money)
        return Response(money_ser.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class EquippedView(APIView):
    def get(self, request):
        char = request.query_params.get('char')

        if not char:
            char = Characters.objects.get(user=request.user)
        else:
            char = Characters.objects.get(id=char)

        equipped = Equipped.objects.get(char=char)
        equip_ser = EquippedSerializer(equipped)
        return Response(equip_ser.data, status=200)

    def post(self, request):
        item_id = request.data.get('item_id')
        char = Characters.objects.get(user=request.user)
        equipped = Equipped.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        try:
            item = Item.objects.get(id=item_id)
            if item.type == '1':
                if equipped.hand:
                    f_remove_properties(properties, equipped.hand)
                equipped.hand = item
            elif item.type == '2':
                if equipped.head:
                    f_remove_properties(properties, equipped.head)
                equipped.head = item
            elif item.type == '3':
                if equipped.shirt:
                    f_remove_properties(properties, equipped.shirt)
                equipped.shirt = item
            elif item.type == '4':
                if equipped.trousers:
                    f_remove_properties(properties, equipped.trousers)
                equipped.trousers = item
            else:
                return Response("Mustn't equip this item.", status=400)

            f_add_properties(properties, item)
            equipped.save()
            return Response("Equip successful.", status=200)
        except Exception as e:
            return Response(str(e), status=400)

    def delete(self, request):
        type = request.query_params.get('type')
        char = Characters.objects.get(user=request.user)
        equipped = Equipped.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        try:
            if type == '1':
                f_remove_properties(properties, equipped.hand)
                equipped.hand = None
            elif type == '2':
                f_remove_properties(properties, equipped.head)
                equipped.head = None
            elif type == '3':
                f_remove_properties(properties, equipped.shirt)
                equipped.shirt = None
            elif type == '4':
                f_remove_properties(properties, equipped.trousers)
                equipped.trousers = None
            else:
                return Response("Type unable!", status=400)

            equipped.save()
            return Response("Remove successful.", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def useItem(request, id):
    try:
        item = Item.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)
        bag = Bag.objects.get(char=char)

        if item.type == "5":
            f_add_properties(properties, item)
            f_removeItemfromBag(bag, item)
            return Response("Use successful!", status=200)
        else:
            return Response("Type unable!", status=400)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def buyItem(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        money = Money.objects.get(char=char)

        money.money -= item.price
        if money.money < 0:
            return Response("Money not enough.", status=400)
        money.save()
        f_addItemtoBag(bag, item)

        return Response("Buy item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sellItem(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        item = Item.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        money = Money.objects.get(char=char)

        f_removeItemfromBag(bag, item)
        money.money += item.price * 0.75
        money.save()

        return Response("Sell item successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def buyBook(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        book = Book.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        money = Money.objects.get(char=char)

        money.money -= book.price
        if money.money < 0:
            return Response("Money not enough.", status=400)
        money.save()
        f_addBooktoBag(bag, book)

        return Response("Buy book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sellBook(request, id):
    try:
        char = Characters.objects.get(user=request.user)
        book = Book.objects.get(id=id)
        bag = Bag.objects.get(char=char)
        money = Money.objects.get(char=char)

        f_removeBookfromBag(bag, book)
        money.money += book.price * 0.75
        money.save()

        return Response("Sell book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@permission_classes([permissions.IsAuthenticated])
class StudyView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        study = Study.objects.get(char=char)
        study_ser = StudySerializer(study)
        return Response(study_ser.data, status=200)

    def post(self, request):
        book_id = request.data.get('book')
        book = Book.objects.get(id=book_id)
        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)

        if properties.canh_gioi < book.level:
            return Response("Level not enough!", status=400)
        try:
            StudyProcess.objects.get(char=char, book=book)
        except:
            StudyProcess.objects.create(char=char, book=book)
        return Response("Start study", status=200)


@permission_classes([permissions.IsAuthenticated])
class StudyProcessView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        study_process = StudyProcess.objects.filter(char=char)
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(study_process, request)
        study_ser = StudyProcessSerializer(page, many=True)
        return pagination.get_paginated_response(study_ser.data)


@permission_classes([permissions.IsAuthenticated])
class StudyProcessDetailView(APIView):
    def get(self, request, id):
        study_process = StudyProcess.objects.get(id=id)
        study_process_ser = StudyProcessSerializer(study_process)
        return Response(study_process_ser.data, status=200)

    def post(self, request, id):
        time = request.data.get('time')
        item = request.data.get('item')

        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)
        study = Study.objects.get(char=char)
        study_process = StudyProcess.objects.get(id=id)
        bag = Bag.objects.get(char=char)

        if item:
            item = Item.objects.get(id=item)
            f_removeItemfromBag(bag, item)
            if item.type == '7':
                study_process.process += 10
        else:
            study_process.process += int(time)
        study_process.save()

        if study_process.process >= study_process.book.duration:
            study.book.add(study_process.book)
            f_add_properties(properties, study_process.book)
            study.save()
            study_process.delete()
            return Response("Study successful!", status=200)
        study_process_ser = StudyProcessSerializer(study_process)
        return Response(study_process_ser.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class KnowledgeView(APIView):
    def get(self, request):
        char = Characters.objects.get(user=request.user)
        knowledge = Knowledge.objects.get(char=char)
        know_ser = KnowledgeSerializer(knowledge)
        return Response(know_ser.data, status=200)

    def post(self, request):
        menu_id = request.data.get('menu_id')
        try:
            char = Characters.objects.get(user=request.user)
            knowledge = Knowledge.objects.get(char=char)
            money = Money.objects.get(char=char)
            properties = Properties.objects.get(char=char)
            menu = Menu.objects.get(id=menu_id)

            if money.dedication - menu.price < 0:
                return Response('You have not enough dedication', status=400)
            money.dedication -= menu.price
            money.save()
            knowledge.menu.add(menu)
            knowledge.save()

            if menu.type == '1':
                properties.luyen_khi += 1
            elif menu.type == '2':
                properties.luyen_dan += 1
            properties.save()

            return Response("Read successful!", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def LevelUpView(request):
    r = request.query_params.get('r')
    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)

    if properties.canh_gioi == 7:
        return Response('Limit canh_gioi', status=400)

    if properties.linh_luc < properties.linh_luc_yeu_cau:
        return Response('linh_luc not enough!', status=400)

    if properties.may_man > 100:
        rate_1 = 100
    else:
        rate_1 = properties.may_man

    if r:
        rate_2 = int(r)*10
    rate_final = int((rate_1 + rate_2)/2)

    num_rand = random.randint(0, 100)
    if num_rand <= rate_final:
        properties.linh_luc = 0
        properties.canh_gioi += 1
        properties.linh_luc_yeu_cau += 200 * properties.canh_gioi

        properties.tuoi_tho += 50 * properties.canh_gioi
        properties.tam_tinh = 100
        properties.suc_khoe = 10

        properties.mau_huyet += 100 * properties.canh_gioi
        properties.cong_kich += 10 * properties.canh_gioi
        properties.phong_ngu += 1 * properties.canh_gioi
        properties.toc_do += 1 * properties.canh_gioi

        properties.save()
        return Response("Level up!", status=200)
    else:
        properties.linh_luc = 0
        properties.tam_tinh = 10
        properties.suc_khoe = 10
        properties.tuoi_tho -= 10
        properties.save()
        return Response("Level up fail!", status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getRank(request):
    type = request.query_params.get('type')
    pagination = PageNumberPagination()
    if type == '1':
        money = Money.objects.all().order_by('-money')
        page = pagination.paginate_queryset(money, request)
        results = MoneySerializer(page, many=True)

    elif type == '2':
        dedication = Money.objects.all().order_by('-dedication')
        page = pagination.paginate_queryset(dedication, request)
        results = MoneySerializer(page, many=True)

    elif type == '3':
        tower = Tower.objects.all().order_by('-floor')
        page = pagination.paginate_queryset(tower, request)
        results = TowerSerializer(page, many=True)

    return pagination.get_paginated_response(results.data)


@permission_classes([permissions.IsAuthenticated])
class RelationshipView(APIView):
    def get(self, request):
        partner = request.query_params.get('partner')
        if partner:
            char_1 = Characters.objects.get(user=request.user)
            char_2 = Characters.objects.get(id=partner)

            try:
                relation = Relationship.objects.get(char1=char_1, char2=char_2)
            except:
                try:
                    relation = Relationship.objects.get(
                        char1=char_2, char2=char_1)
                except:
                    relation = Relationship.objects.create(
                        char1=char_1, char2=char_2)
            relation_ser = RelationshipSerializer(relation)
            return Response(relation_ser.data, status=200)

        else:
            char = Characters.objects.get(user=request.user)
            relation = Relationship.objects.filter(
                Q(char1=char) | Q(char2=char))
            pagination = PageNumberPagination()
            page = pagination.paginate_queryset(relation, request)
            relation_ser = RelationshipSerializer(page, many=True)
            return pagination.get_paginated_response(relation_ser.data)

    def post(self, request):
        partner = request.data.get('partner')
        item_id = request.data.get('item_id')

        char_1 = Characters.objects.get(user=request.user)
        char_2 = Characters.objects.get(id=partner)
        item = Item.objects.get(id=item_id)
        bag = Bag.objects.get(char=char_1)
        try:
            relation = Relationship.objects.get(char1=char_1, char2=char_2)
        except:
            try:
                relation = Relationship.objects.get(char1=char_2, char2=char_1)
            except:
                relation = Relationship.objects.create(
                    char1=char_1, char2=char_2)
        f_removeItemfromBag(bag, item)
        relation.point += 10
        relation.save()
        relation_ser = RelationshipSerializer(relation)
        return Response(relation_ser.data, status=200)

    def delete(self, request):
        partner = request.query_params.get('partner')
        char_1 = Characters.objects.get(user=request.user)
        char_2 = Characters.objects.get(id=partner)

        try:
            relation = Relationship.objects.get(char1=char_1, char2=char_2)
        except:
            try:
                relation = Relationship.objects.get(char1=char_2, char2=char_1)
            except:
                relation = Relationship.objects.create(
                    char1=char_1, char2=char_2)
        relation.point -= 10
        relation.save()
        relation_ser = RelationshipSerializer(relation)
        return Response(relation_ser.data, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def restore(request):
    money_spend = request.data.get('money')

    char = Characters.objects.get(user=request.user)
    properties = Properties.objects.get(char=char)
    money = Money.objects.get(char=char)

    money.money -= int(money_spend)
    if money.money < 0:
        return Response("Money not enough!", status=400)
    money.save()

    properties.tam_tinh += int(int(money_spend)/500)
    if properties.tam_tinh > 100:
        properties.tam_tinh = 100
    properties.suc_khoe += int(int(money_spend)/500)
    if properties.suc_khoe > 100:
        properties.suc_khoe = 100
    properties.save()

    return Response({
        'suc_khoe': int(int(money_spend)/500),
        'tam_tinh': int(int(money_spend)/500)
    }, status=200)
