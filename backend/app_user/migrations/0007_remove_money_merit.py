# Generated by Django 5.0.4 on 2024-05-24 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0006_ownpet_properties_delete_ownmaid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='money',
            name='merit',
        ),
    ]
