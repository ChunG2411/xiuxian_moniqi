# Generated by Django 4.1.3 on 2024-03-27 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_clan', '0004_clan_image_organization_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clan',
            options={'ordering': ['level'], 'verbose_name': 'Môn phái'},
        ),
    ]