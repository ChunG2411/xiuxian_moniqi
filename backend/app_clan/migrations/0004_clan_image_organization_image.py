# Generated by Django 4.1.3 on 2024-03-27 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_clan', '0003_remove_organization_exp_remove_organization_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clan',
            name='image',
            field=models.ImageField(blank=True, default='temp/item.jpg', null=True, upload_to='clan'),
        ),
        migrations.AddField(
            model_name='organization',
            name='image',
            field=models.ImageField(blank=True, default='temp/item.jpg', null=True, upload_to='organization'),
        ),
    ]
