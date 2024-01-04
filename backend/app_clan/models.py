from django.db import models

from app_user.models import Characters

# Create your models here.
class Clan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    member = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    exp_request = models.IntegerField(default=100)

    class Meta:
        db_table = 'tb_clan'
        verbose_name = 'Môn phái'


class ClanPosition(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="ClanPosition_char")
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="ClanPosition_clan")
    position = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_clan_position'
        verbose_name = 'Chức vị môn phái'


class RequestClan(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="RequestClan_char")
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="RequestClan_clan")

    class Meta:
        db_table = 'tb_request_clan'
        verbose_name = 'Yêu cầu gia nhập'


class OnlineClan(models.Model):
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="OnlineClan_clan")
    char = models.ManyToManyField(Characters, blank=True, related_name="OnlineClan_char")
    
    class Meta:
        db_table = 'tb_online_clan'
        verbose_name = 'Thành viên môn phái có mặt'
