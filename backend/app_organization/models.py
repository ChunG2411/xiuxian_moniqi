from django.db import models
from app_user.models import Characters

import uuid

# Create your models here.

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    image = models.ImageField(blank=True, default="temp/item.jpg", null=True, upload_to="organization")
    member = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_organization'
        verbose_name = 'Thế lực'


class Locality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, unique=True, related_name="Locality_char")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="Locality_organization")
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    defender = models.IntegerField(default=1000)
    power = models.IntegerField(default=200)
    time_protect = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_locality'
        verbose_name = 'Địa bàn'


class Mine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    owner = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, related_name="Mine_locality")
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    defender = models.IntegerField(default=2000)
    produce = models.IntegerField(default=2)
    store = models.IntegerField(default=0)
    limit = models.IntegerField(default=200)
    get_at = models.DateTimeField(auto_now=True)
    time_protect = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_mine'
        verbose_name = 'Mỏ quặng'


class Market(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    owner = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, related_name="Market_locality")
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    defender = models.IntegerField(default=1000)
    produce = models.IntegerField(default=1)
    store = models.IntegerField(default=0)
    limit = models.IntegerField(default=100)
    get_at = models.DateTimeField(auto_now=True)
    time_protect = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_market'
        verbose_name = 'Khu buôn bán'
