# Generated by Django 4.1.3 on 2024-04-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0006_ownpet_properties_delete_ownmaid'),
        ('app_item', '0003_remove_book_attribute'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Maid',
        ),
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ImageField(blank=True, default='temp/item.jpg', null=True, upload_to='pet'),
        ),
        migrations.AddField(
            model_name='pet',
            name='properties',
            field=models.JSONField(default=dict),
        ),
    ]
