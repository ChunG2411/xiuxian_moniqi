# Generated by Django 4.1.3 on 2024-03-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0004_money_merit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='cong_kich',
            field=models.IntegerField(default=2, verbose_name='công kích'),
        ),
        migrations.AlterField(
            model_name='properties',
            name='mau_huyet',
            field=models.IntegerField(default=10, verbose_name='máu huyết'),
        ),
    ]