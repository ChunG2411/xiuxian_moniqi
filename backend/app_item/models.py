from django.db import models
from xiuxian_moniqi.config import TYPE_ITEM, TYPE_MENU, ATTRIBUTE

import uuid
# Create your models here.


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    descripstion = models.TextField(default="")
    image = models.ImageField(blank=True, default="temp/item.jpg", null=True, upload_to="item")
    type = models.CharField(max_length=10, choices=TYPE_ITEM, default='1')
    price = models.IntegerField(default=0)
    quality = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    properties = models.JSONField(default=dict)

    class Meta:
        db_table = 'tb_item'
        verbose_name = 'Vật phẩm'


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    descripstion = models.TextField(default="")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="Menu_item")
    materials = models.ManyToManyField(Item, blank=True, related_name="Menu_materials")
    type = models.CharField(max_length=10, choices=TYPE_MENU, default='1')
    price = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_menu'
        verbose_name = 'Công thức'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    descripstion = models.TextField(default="")
    level = models.IntegerField(default=1)
    quality = models.IntegerField(default=1)
    attribute = models.CharField(max_length=10, choices=ATTRIBUTE, default='1')
    properties = models.JSONField(default=dict)
    price = models.IntegerField(default=1)
    duration = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_book'
        verbose_name = 'Công pháp'


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    descripstion = models.TextField(default="")
    quality = models.IntegerField(default=1)
    price = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_pet'
        verbose_name = 'Sủng vật'


class Maid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    descripstion = models.TextField(default="")
    quality = models.IntegerField(default=1)
    price = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_maid'
        verbose_name = 'Người hầu'