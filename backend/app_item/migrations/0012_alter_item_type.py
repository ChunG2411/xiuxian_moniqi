# Generated by Django 4.2.5 on 2023-12-28 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_item", "0011_alter_item_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="type",
            field=models.CharField(
                choices=[
                    ("1", "equip hand"),
                    ("2", "equip foot"),
                    ("3", "equip shirt"),
                    ("4", "equip trousers"),
                    ("5", "food"),
                    ("6", "material1"),
                    ("7", "material2"),
                    ("8", "lucky"),
                ],
                default="1",
                max_length=10,
            ),
        ),
    ]