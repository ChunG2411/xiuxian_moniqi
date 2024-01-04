import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    User,
    Characters,
    Gifted,
    Properties,
    Bag,
    Equipped,
    Money,
    Knowledge,
    Study,
    Relationship
    )

from .serializers import (
    UserRegisterSerializers,
    CharactersSerializers,
    GiftedSerializer,
    BagSerializer,
    MoneySerializer,
    EquippedSerializer,
    KnowledgeSerializer,
    StudySerializer,
    RelationshipSerializer
    )
from app_item.models import Item, Menu, Book
from app_item.serializers import ItemSerializer
from app_item.views import removeItemfromBag_function
from app_location.models import TowerChallenge, Tower
from app_location.serializers import TowerChallengeSerializer
from xiuxian_moniqi.config import START_TIME

import random
from datetime import datetime, timezone

# from celery.schedules import crontab
# from celery.task import periodic_task

# @periodic_task(run_every=crontab(minute=1))
# def function():
#     print("1")

# Create your views here.
def add_properties(properties, item):
    properties_dict = dict(item.properties)
    for j in properties_dict:
        old_value = getattr(properties, j)
        setattr(properties, j, old_value + properties_dict[j])
    properties.save()

def remove_properties(properties, item):
    properties_dict = dict(item.properties)
    for j in properties_dict:
        old_value = getattr(properties, j)
        setattr(properties, j, old_value - properties_dict[j])
    properties.save()


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegisterSerializers(context={"request": request}, data=request.data)
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
            return Response("Password inccorect.", status=400)

        refresh = TokenObtainPairSerializer.get_token(user)
        user.last_login = datetime.datetime.now()
        user.save()
        response = {
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

        return Response(response, status=201)


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
            char_serializer = CharactersSerializers(context={"request": request}, data=request_copy)
            if char_serializer.is_valid():
                char_serializer.save()
                return Response(char_serializer.data, status=201)
        return Response(char_serializer.errors, status=400)
    
    def delete(self, request):
        try:
            char = Characters.objects.get(user=request.user)
            properties = Properties.objects.get(char=char)
            bag = Bag.objects.get(char=char)
            equipped = Equipped.objects.get(char=char)
            money = Money.objects.get(char=char)

            bag.delete()
            properties.delete()
            char.delete()
            equipped.delete()
            money.delete()
            
            return Response("Delete successfull!", status=200)
        except Exception as e:
            return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getCurrChar(request):
    try:
        now = datetime.now(timezone.utc)
        start_time = datetime.strptime(START_TIME, "%d-%m-%Y %H:%M:%S").replace(tzinfo=timezone.utc)
        duration = now - start_time
        duration_year = duration / 365

        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)

        if properties.tuoi > properties.tuoi_tho:
            return Response("The lifespan limit has been reached", status=202)
        
        char_ser = CharactersSerializers(char)
        return Response(char_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getGiftedList(request):
    gifted = Gifted.objects.all()
    gifted_ser = GiftedSerializer(gifted, many=True)
    return Response(gifted_ser.data, status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getGiftedDetail(request, id):
    try:
        gifted = Gifted.objects.get(id=id)
        gifted_ser = GiftedSerializer(gifted)
        return Response(gifted_ser.data, status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBag(request):
    char = Characters.objects.get(user=request.user)
    bag = Bag.objects.get(char=char)
    bag_ser = BagSerializer(bag)
    return Response(bag_ser.data, status=200)


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
        char = Characters.objects.get(user=request.user)
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
                    remove_properties(properties, equipped.hand)
                equipped.hand = item
            elif item.type == '2':
                if equipped.foot:
                    remove_properties(properties, equipped.foot)
                equipped.foot = item
            elif item.type == '3':
                if equipped.shirt:
                    remove_properties(properties, equipped.shirt)
                equipped.shirt = item
            elif item.type == '4':
                if equipped.trousers:
                    remove_properties(properties, equipped.trousers)
                equipped.trousers = item
            else:
                return Response("Don't equip this item", status=400)

            add_properties(properties, item)
            equipped.save()
            
            return Response("Use successful.", status=200)
        except Exception as e:
            return Response(str(e), status=400)
    
    def delete(self, request):
        type = request.query_params.get('type')
        char = Characters.objects.get(user=request.user)
        equipped = Equipped.objects.get(char=char)
        properties = Properties.objects.get(char=char)
        try:
            if type == '1':
                remove_properties(properties, equipped.hand)
                equipped.hand = None
            elif type == '2':
                remove_properties(properties, equipped.foot)
                equipped.foot = None
            elif type == '3':
                remove_properties(properties, equipped.shirt)
                equipped.shirt = None
            elif type == '4':
                remove_properties(properties, equipped.trousers)
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
            add_properties(properties, item)
            try:
                bag.items[str(item.id)] -= 1
                if bag.items[str(item.id)] <= 0:
                    del bag.items[str(item.id)]
            except:
                del bag.items[str(item.id)]
            bag.save()
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
        try:
            bag.items[str(item.id)] += 1
        except:
            bag.items[str(item.id)] = 1
        bag.save()
        money.money -= item.price
        money.save()
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

        try:
            bag.items[str(item.id)]
        except:
            return Response("Don't have item!", status=200)
        
        try:
            bag.items[str(item.id)] -= 1
            if bag.items[str(item.id)] <= 0:
                del bag.items[str(item.id)]
        except:
            del bag.items[str(item.id)]
        bag.save()
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
        try:
            bag.books[str(book.id)] += 1
        except:
            bag.books[str(book.id)] = 1
        bag.save()
        money.money -= book.price
        money.save()
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

        try:
            bag.books[str(book.id)]
        except:
            return Response("Don't have item!", status=200)
        
        try:
            bag.books[str(book.id)] -= 1
            if bag.books[str(book.id)] <= 0:
                del bag.books[str(book.id)]
        except:
            del bag.books[str(book.id)]
        bag.save()
        money.money += book.price * 0.75
        money.save()

        return Response("Sell book successful!", status=200)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getStudy(request):
    char = Characters.objects.get(user=request.user)
    study = Study.objects.get(char=char)
    study_ser = StudySerializer(study)
    return Response(study_ser.data, status=200)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def studyBook(request, id):
    r = request.data.get('r')
    try:
        book = Book.objects.get(id=id)
        char = Characters.objects.get(user=request.user)
        properties = Properties.objects.get(char=char)
        study = Study.objects.get(char=char)
        bag = Bag.objects.get(char=char)
        
        if str(book.id) not in bag.books:
            return Response("You don't have this book", status=400)
        
        if properties.canh_gioi < book.level:
            return Response("Level not enough!", status=400)

        if book.attribute == '1':
            rate_1 = properties.hoa_linh_can
        elif book.attribute == '2':
            rate_1 = properties.thuy_linh_can
        elif book.attribute == '3':
            rate_1 = properties.tho_linh_can
        elif book.attribute == '4':
            rate_1 = properties.moc_linh_can
        elif book.attribute == '5':
            rate_1 = properties.phong_linh_can
        elif book.attribute == '6':
            rate_1 = properties.loi_linh_can
        
        rate_2 = int(r) * 10
        if rate_1 > 100: rate_1 = 100
        rate_final = (rate_1 + rate_2)/2
        
        if random.randint(0, 100) <= rate_final:
            add_properties(properties, book)
            try:
                bag.books[str(book.id)] -= 1
                if bag.books[str(book.id)] <= 0:
                    del bag.books[str(book.id)]
            except:
                del bag.books[str(book.id)]
            bag.save()
            study.book.add(book)
            study.save()
            return Response("Study successful!", status=200)
        else:
            try:
                bag.books[str(book.id)] -= 1
                if bag.books[str(book.id)] <= 0:
                    del bag.books[str(book.id)]
            except:
                del bag.books[str(book.id)]
            bag.save()
            return Response("Study fail!", status=200)

    except Exception as e:
        return Response(str(e), status=400)
    

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
            menu = Menu.objects.get(id=menu_id)
            knowledge.menu.add(menu)
            knowledge.save()

            properties = Properties.objects.get(char=char)
            if menu.type == '1':
                properties.luyen_khi += 1
            elif menu.type == '2':
                properties.luyen_dan += 1
            elif menu.type == '3':
                properties.hoa_phu += 1
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
    
    if properties.linh_luc < properties.linh_luc_yeu_cau:
        return Response('linh_luc not enough!', status=400)
    
    if properties.may_man > 100:
        rate_1 = 100
    else: rate_1 = properties.may_man

    if properties.ngo_tinh > 100:
        rate_2 = 100
    else: rate_2 = properties.ngo_tinh
    
    if r:
        rate_3 = int(r)*10
    else: rate_3 = 0
    rate_final = int((rate_1 + rate_2 + rate_3)/3)
    
    num_rand = random.randint(0, 100)
    if num_rand <= rate_final:
        properties.linh_luc = 0
        properties.canh_gioi += 1
        properties.linh_luc_yeu_cau += 200 * properties.canh_gioi

        properties.tuoi_tho += 50 * properties.canh_gioi
        properties.tam_tinh += 100 * properties.canh_gioi
        properties.niem_luc += 5 * properties.canh_gioi
        properties.suc_khoe = 10

        properties.mau_huyet += 100 * properties.canh_gioi
        properties.cong_kich += 10 * properties.canh_gioi
        properties.phong_ngu += 1 * properties.canh_gioi
        properties.toc_do += 1 * properties.canh_gioi
        properties.khang_cong += 1 * properties.canh_gioi
        properties.khang_linh += 1 * properties.canh_gioi
        properties.bao_kich += 1 * properties.canh_gioi
        properties.khang_bao += 1 * properties.canh_gioi
        properties.ne_tranh += 1 * properties.canh_gioi

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
    
    if type == 'money':
        money = Money.objects.all().order_by('-money')
        results = MoneySerializer(money, many=True)
    elif type == 'dedication':
        dedication = Money.objects.all().order_by('-dedication')
        results = MoneySerializer(dedication, many=True)
    else:
        tower = Tower.objects.get(id=type)
        challenge = TowerChallenge.objects.filter(tower=tower).order_by('-floor')
        results = TowerChallengeSerializer(challenge, many=True)
    
    return Response(results.data, status=200)


@permission_classes([permissions.IsAuthenticated])
class RelationshipView(APIView):
    def get(self, request):
        partner = request.query_params.get('partner')
        char_1 = Characters.objects.get(user=request.user)
        char_2 = Characters.objects.get(id=partner)

        try:
            relation = Relationship.objects.get(char1=char_1, char2=char_2)
        except:
            try:
                relation = Relationship.objects.get(char1=char_2, char2=char_1)
            except:
                relation = Relationship.objects.create(char1=char_1, char2=char_2)
        relation_ser = RelationshipSerializer(relation)
        return Response(relation_ser.data, status=200)
    
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
                relation = Relationship.objects.create(char1=char_1, char2=char_2)
        removeItemfromBag_function(bag, item)
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
                relation = Relationship.objects.create(char1=char_1, char2=char_2)
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
