from django.db import models

from app_user.models import Characters

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.IntegerField(default=1)
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_city'
        verbose_name = 'Thành trì'


class OnlineCity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="OnlineCity_clan")
    char = models.ManyToManyField(Characters, blank=True, related_name="OnlineCity_char")
    
    class Meta:
        db_table = 'tb_online_city'
        verbose_name = 'Người nhập thành'


class Tower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.IntegerField(default=1)
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_tower'
        verbose_name = 'Tháp'


class TowerChallenge(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="TowerChallenge_char")
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, related_name="TowerChallenge_tower")
    floor = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_tower_challenge'
        verbose_name = 'Tháp khiêu chiến'


class ChallengeBoard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    rank = models.JSONField(default=dict)

    class Meta:
        db_table = 'tb_challenge_board'
        verbose_name = 'Bảng khiêu chiến'