from django.db import models
from app_user.models import Characters

import uuid

# Create your models here.
class Clan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    leader = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="Clan_leader")
    member = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_clan'
        verbose_name = 'Môn phái'


class ClanPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="ClanPosition_char")
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="ClanPosition_clan")
    position = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_clan_position'
        verbose_name = 'Chức vị môn phái'


class RequestClan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="RequestClan_char")
    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name="RequestClan_clan")

    class Meta:
        db_table = 'tb_request_clan'
        verbose_name = 'Yêu cầu gia nhập môn phái'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    member = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_organization'
        verbose_name = 'Thế lực'


class OrganizationPosition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="OrganizationPosition_char")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="OrganizationPosition_organization")
    position = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_organization_position'
        verbose_name = 'Chức vị thế lực'
