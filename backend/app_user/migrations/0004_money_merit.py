# Generated by Django 4.1.3 on 2024-03-26 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_remove_properties_hoa_thuoc_tinh_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='merit',
            field=models.IntegerField(default=0),
        ),
    ]
