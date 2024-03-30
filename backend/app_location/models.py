from django.db import models
from app_user.models import Characters

import uuid


# Create your models here.

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    quality = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_city'
        verbose_name = 'Thành trì'


class Tower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="TowerChallenge_char")
    floor = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_tower'
        verbose_name = 'Tháp khiêu chiến'


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    number = models.IntegerField()
    question = models.TextField()
    answer_1 = models.TextField()
    answer_2 = models.TextField()
    answer_3 = models.TextField()
    answer_correct = models.IntegerField(default=1)

    class Meta:
        db_table = 'tb_question'
        verbose_name = 'Danh sách câu hỏi'


class QuestionChar(models.Model):
    char = models.ForeignKey(Characters, on_delete=models.CASCADE, related_name="QuestionChar_char")
    question = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_question_char'
        verbose_name = 'Câu hỏi'