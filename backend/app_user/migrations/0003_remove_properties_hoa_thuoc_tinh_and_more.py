# Generated by Django 4.1.3 on 2024-03-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_alter_studyprocess_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='properties',
            name='hoa_thuoc_tinh',
        ),
        migrations.RemoveField(
            model_name='properties',
            name='khoang_san',
        ),
        migrations.RemoveField(
            model_name='properties',
            name='kim_thuoc_tinh',
        ),
        migrations.RemoveField(
            model_name='properties',
            name='moc_thuoc_tinh',
        ),
        migrations.RemoveField(
            model_name='properties',
            name='tho_thuoc_tinh',
        ),
        migrations.RemoveField(
            model_name='properties',
            name='thuy_thuoc_tinh',
        ),
        migrations.AddField(
            model_name='properties',
            name='power',
            field=models.IntegerField(default=0),
        ),
    ]