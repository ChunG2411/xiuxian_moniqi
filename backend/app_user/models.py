from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from .managers import CustomUserManager
from xiuxian_moniqi.config import GENDER
from app_item.models import Item, Menu, Book, Pet, Maid

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


class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
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
    appearance = models.ImageField(upload_to='appearance', null=True, blank=True, default='temp/avatar.png')
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
    power = models.IntegerField(default=0)

    tuoi = models.IntegerField(default=1, verbose_name="tuổi")
    tuoi_tho = models.IntegerField(default=80, verbose_name="tuổi thọ")
    tam_tinh = models.IntegerField(default=10, verbose_name="tâm tình")
    suc_khoe = models.IntegerField(default=10, verbose_name="sức khỏe")

    mau_huyet = models.IntegerField(default=10, verbose_name="máu huyết")
    cong_kich = models.IntegerField(default=2, verbose_name="công kích")
    phong_ngu = models.IntegerField(default=1, verbose_name="phòng ngự")
    toc_do = models.IntegerField(default=1, verbose_name="tốc độ")

    luyen_khi = models.IntegerField(default=0, verbose_name="luyện khí")
    luyen_dan = models.IntegerField(default=0, verbose_name="luyện đan")
    duoc_lieu = models.IntegerField(default=0, verbose_name="dược liệu")
    may_man = models.IntegerField(default=0, verbose_name="may mắn")

    class Meta:
        db_table = 'tb_properties'
        verbose_name = 'Thuộc tính'
    
    def save(self, *args, **kwargs):
        self.power = self.mau_huyet + self.cong_kich + self.phong_ngu + self.toc_do
        super().save(*args, **kwargs)


class Bag(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Bag_characters")
    items = models.JSONField(default=dict)
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
    head = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_head")
    shirt = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_shirt")
    trousers = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Equipped_trousers")
    
    class Meta:
        db_table = 'tb_equipped'
        verbose_name = 'Trang bị'


class Money(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Money_characters")
    money = models.IntegerField(default=0)
    dedication = models.IntegerField(default=0)
    merit = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_money'
        verbose_name = 'Tiền tệ'


class Study(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Study_characters")
    book = models.ManyToManyField(Book, blank=True, related_name="Study_book")

    class Meta:
        db_table = 'tb_study'
        verbose_name = 'Công pháp lĩnh ngộ'


class StudyProcess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="StudyProcess_characters")
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE, related_name="StudyProcess_book")
    process = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_study_process'
        verbose_name = 'Lĩnh ngộ công pháp'
    

class OwnPet(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="OwnPet_char")
    pet = models.ForeignKey(Pet, null=True, on_delete=models.CASCADE, related_name="OwnPet_pet")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_own_pet'
        verbose_name = 'Nuôi thú'


class OwnMaid(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="OwnMaid_char")
    maid = models.ForeignKey(Maid, null=True, on_delete=models.CASCADE, related_name="OwnMaid_maid")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_own_maid'
        verbose_name = 'Nuôi người hầu'


class Relationship(models.Model):
    char1 = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Relationship_char1")
    char2 = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Relationship_char2")
    point = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_relationship'
        verbose_name = 'Mối quan hệ'

