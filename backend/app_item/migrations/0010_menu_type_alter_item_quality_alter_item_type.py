# Generated by Django 4.2.5 on 2023-12-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_item", "0009_alter_item_quality_alter_item_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="type",
            field=models.CharField(
                choices=[("1", "luyen_khi"), ("2", "luyen_dan"), ("3", "hoa_phu")],
                default="1",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="quality",
            field=models.CharField(
                choices=[
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                    ("6", "6"),
                    ("7", "7"),
                    ("8", "8"),
                    ("9", "9"),
                    ("10", "10"),
                ],
                default="1",
                max_length=10,
            ),
        ),
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
