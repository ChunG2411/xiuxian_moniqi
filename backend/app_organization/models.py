from django.db import models
from app_user.models import Characters
from xiuxian_moniqi.config import LOCALITY, MARKET, MINE
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
    name = models.CharField(max_length=100, default='')
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    defender = models.IntegerField(default=LOCALITY['defender'])
    power = models.IntegerField(default=LOCALITY['power'])
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
    defender = models.IntegerField(default=MINE['defender'])
    produce = models.IntegerField(default=MINE['produce'])
    store = models.IntegerField(default=0)
    limit = models.IntegerField(default=MINE['limit'])
    get_at = models.DateTimeField(null=True)
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
    defender = models.IntegerField(default=MARKET['defender'])
    produce = models.IntegerField(default=MARKET['produce'])
    store = models.IntegerField(default=0)
    limit = models.IntegerField(default=MARKET['limit'])
    get_at = models.DateTimeField(null=True)
    time_protect = models.DateTimeField(null=True)

    class Meta:
        db_table = 'tb_market'
        verbose_name = 'Khu buôn bán'


class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True, related_name="Mail_sender")
    receiver = models.ForeignKey(Locality, on_delete=models.CASCADE, null=True, related_name="Mail_receiver")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_mail'
        verbose_name = 'Thư thế lực'
        ordering = ['-created_at']
        