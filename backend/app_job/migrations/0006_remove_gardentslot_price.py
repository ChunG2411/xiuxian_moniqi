# Generated by Django 4.2.5 on 2023-12-29 02:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app_job", "0005_gardent_exp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gardentslot",
            name="price",
        ),
    ]