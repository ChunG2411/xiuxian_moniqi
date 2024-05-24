# Generated by Django 5.0.4 on 2024-05-24 07:44

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locality',
            name='resources',
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('pos_x', models.IntegerField(default=0)),
                ('pos_y', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('defender', models.IntegerField(default=1000)),
                ('produce', models.IntegerField(default=1)),
                ('store', models.IntegerField(default=100)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Market_locality', to='app_organization.locality')),
            ],
            options={
                'verbose_name': 'Khu buôn bán',
                'db_table': 'tb_market',
            },
        ),
        migrations.CreateModel(
            name='Mine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('pos_x', models.IntegerField(default=0)),
                ('pos_y', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('defender', models.IntegerField(default=1000)),
                ('produce', models.IntegerField(default=1)),
                ('store', models.IntegerField(default=100)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Mine_locality', to='app_organization.locality')),
            ],
            options={
                'verbose_name': 'Mỏ quặng',
                'db_table': 'tb_mine',
            },
        ),
    ]
