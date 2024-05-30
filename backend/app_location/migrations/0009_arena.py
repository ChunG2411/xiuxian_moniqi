# Generated by Django 5.0.4 on 2024-05-30 07:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0008_alter_questionchar_char'),
        ('app_user', '0008_chat_delete_relationship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arena',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=1)),
                ('char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Arena_char', to='app_user.characters', unique=True)),
            ],
            options={
                'verbose_name': 'Đấu trường',
                'db_table': 'tb_arena',
                'ordering': ['-number'],
            },
        ),
    ]
