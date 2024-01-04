from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

from .managers import CustomUserManager
from xiuxian_moniqi.config import GENDER, BACKGROUND
from app_item.models import Item, Menu, Book

import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=100, unique=True, validators=[username_validator], default=uuid.uuid4)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'tb_user'
        verbose_name = 'Người dùng'


class Gifted(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default="")
    properties = models.JSONField()

    class Meta:
        db_table = 'tb_gifted'
        verbose_name = 'Tiên thiên khí vận'


class Title(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default="")

    class Meta:
        db_table = 'tb_title'
        verbose_name = 'Danh hiệu'


class Characters(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Characters_user")
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER)
    appearance = models.ImageField(upload_to='avatar', null=True, blank=True, default='temp/avatar.png')
    background = models.CharField(max_length=10, choices=BACKGROUND)
    gifted = models.ManyToManyField(Gifted, blank=True, related_name="Characters_gifted")
    title = models.ManyToManyField(Title, blank=True, related_name="Characters_title")
    date_join = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_characters'
        verbose_name = 'Nhân vật'


class Properties(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Properties_characters")

    canh_gioi = models.IntegerField(default=1)
    linh_luc = models.IntegerField(default=0)
    linh_luc_yeu_cau = models.IntegerField(default=100)

    tuoi = models.IntegerField(default=10, verbose_name="tuổi")
    tuoi_tho = models.IntegerField(default=80, verbose_name="tuổi thọ")
    tam_tinh = models.IntegerField(default=50, verbose_name="tâm tình")
    suc_khoe = models.IntegerField(default=50, verbose_name="sức khỏe")

    niem_luc = models.IntegerField(default=0, verbose_name="niệm lực")
    may_man = models.IntegerField(default=1, verbose_name="may mắn")
    ngo_tinh = models.IntegerField(default=1, verbose_name="ngộ tính")
    danh_vong = models.IntegerField(default=0, verbose_name="danh vọng")
    mi_luc = models.IntegerField(default=1, verbose_name="mị lực")
    sat_khi = models.IntegerField(default=0, verbose_name="sát khí")

    mau_huyet = models.IntegerField(default=100, verbose_name="máu huyết")
    cong_kich = models.IntegerField(default=10, verbose_name="công kích")
    phong_ngu = models.IntegerField(default=1, verbose_name="phòng ngự")
    toc_do = models.IntegerField(default=1, verbose_name="tốc độ")
    khang_cong = models.IntegerField(default=1, verbose_name="kháng công")
    khang_linh = models.IntegerField(default=1, verbose_name="kháng linh")
    bao_kich = models.IntegerField(default=0, verbose_name="bạo kích")
    khang_bao = models.IntegerField(default=0, verbose_name="kháng bạo")
    ne_tranh = models.IntegerField(default=0, verbose_name="né tránh")

    hoa_linh_can = models.IntegerField(default=1, verbose_name="hỏa linh căn")
    thuy_linh_can = models.IntegerField(default=1, verbose_name="thủy linh căn")
    phong_linh_can = models.IntegerField(default=1, verbose_name="phong linh căn")
    moc_linh_can = models.IntegerField(default=1, verbose_name="mộc linh căn")
    tho_linh_can = models.IntegerField(default=1, verbose_name="thổ linh căn")
    loi_linh_can = models.IntegerField(default=1, verbose_name="lôi linh căn")

    luyen_khi = models.IntegerField(default=0, verbose_name="luyện khí")
    luyen_dan = models.IntegerField(default=0, verbose_name="luyện đan")
    hoa_phu = models.IntegerField(default=0, verbose_name="họa phù")
    duoc_lieu = models.IntegerField(default=0, verbose_name="dược liệu")
    khoang_san = models.IntegerField(default=0, verbose_name="khoáng sản")

    class Meta:
        db_table = 'tb_properties'
        verbose_name = 'Thuộc tính'


class Bag(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Bag_characters")
    items = models.JSONField(default={})
    books = models.JSONField(default=dict)

    class Meta:
        db_table = 'tb_bag'
        verbose_name = 'Túi đồ'


class Knowledge(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Knowledge_char")
    menu = models.ManyToManyField(Menu, blank=True, related_name="Knowledge_menu")

    class Meta:
        db_table = 'tb_knowledge'
        verbose_name = 'Kiến thức'


class Equipped(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Equipped_characters")
    hand = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_hand")
    foot = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_foot")
    shirt = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_shirt")
    trousers = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_trousers")

    class Meta:
        db_table = 'tb_equipped'
        verbose_name = 'Trang bị'


class Money(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Money_characters")
    money = models.IntegerField(default=0)
    dedication = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_money'
        verbose_name = 'Linh thạch'


class Study(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Study_characters")
    book = models.ManyToManyField(Book, blank=True, related_name="Study_book")

    class Meta:
        db_table = 'tb_study'
        verbose_name = 'Công pháp lĩnh ngộ'
    

class Relationship(models.Model):
    char1 = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Relationship_char1")
    char2 = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Relationship_char2")
    point = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_relationship'
        verbose_name = 'Mối quan hệ'

