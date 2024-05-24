# Generated by Django 5.0.4 on 2024-05-24 04:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_clan', '0009_alter_locality_char'),
        ('app_user', '0006_ownpet_properties_delete_ownmaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='char',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Locality_char', to='app_user.characters'),
        ),
    ]
