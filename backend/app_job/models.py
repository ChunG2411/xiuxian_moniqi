from django.db import models

from app_user.models import Characters
from app_item.models import Item
from xiuxian_moniqi.config import TYPE_SEED

import uuid

# Create your models here.


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default="My house")
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="House_char")
    quality = models.IntegerField(default=1)
    store = models.JSONField(default=dict)

    class Meta:
        db_table = 'tb_house'
        verbose_name = 'Động phủ'


class Seed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    image = models.ImageField(blank=True, default="temp/item.jpg", null=True, upload_to="seed")
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Seed_item")
    time = models.IntegerField(default=1)
    price = models.IntegerField(default=1)
    type = models.CharField(max_length=10, choices=TYPE_SEED, default='1')

    class Meta:
        db_table = 'tb_seed'
        verbose_name = 'Hạt giống'


class Gardent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default="My gardent")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Gardent_char")
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_gardent'
        verbose_name = 'Vườn cây'
    

class GardentSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    gardent = models.ForeignKey(Gardent, on_delete=models.CASCADE, related_name="GardentSlot_gardent")
    seed = models.ForeignKey(Seed, null=True, on_delete=models.CASCADE, related_name="GardentSlot_seed")
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_gardent_slot'
        verbose_name = 'Chậu cây'


class Cage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default="My cage")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Cage_char")
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_cage'
        verbose_name = 'Chuồng thú'


class CageSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE, related_name="CageSlot_cage")
    seed = models.ForeignKey(Seed, null=True, on_delete=models.CASCADE, related_name="CageSlot_seed")
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_cage_slot'
        verbose_name = 'Lồng'


class Lake(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, default="My lake")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Lake_char")
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_lake'
        verbose_name = 'Hồ nước'


class LakeSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    lake = models.ForeignKey(Lake, on_delete=models.CASCADE, related_name="LakeSlot_lake")
    seed = models.ForeignKey(Seed, null=True, on_delete=models.CASCADE, related_name="LakeSlot_seed")
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_lake_slot'
        verbose_name = 'Lượng cá'


class Oven(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    level = models.IntegerField(default=1)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Oven_char")

    class Meta:
        db_table = 'tb_oven'
        verbose_name = 'Đan lô'
