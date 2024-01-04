from django.db import models

from app_user.models import Characters
from app_item.models import Item

# Create your models here.
class Seed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="Seed_item")
    time = models.IntegerField(default=1)
    price = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_seed'
        verbose_name = 'Hạt giống'


class Gardent(models.Model):
    name = models.CharField(max_length=100, default="My gardent")
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Gardent_char")
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_gardent'
        verbose_name = 'Vườn cây'
    

class GardentSlot(models.Model):
    gardent = models.ForeignKey(Gardent, on_delete=models.CASCADE, related_name="GardentSlot_gardent")
    level = models.IntegerField(default=1)
    seed = models.ForeignKey(Seed, null=True, on_delete=models.CASCADE, related_name="GardentSlot_plant")
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_gardentslot'
        verbose_name = 'Chậu cây'


class StoreHouse(models.Model):
    name = models.CharField(max_length=100, default="My storehouse")
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="StoreHouse_char")
    seed = models.JSONField(default=dict)

    class Meta:
        db_table = 'tb_storehouse'
        verbose_name = 'Nhà kho'


class House(models.Model):
    name = models.CharField(max_length=100, default="My house")
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="House_char")
    quality = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'tb_house'
        verbose_name = 'Động phủ'


class Mines(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    level = models.IntegerField()

    class Meta:
        db_table = 'tb_mines'
        verbose_name = 'Mỏ quặng'
        ordering = ['level']
