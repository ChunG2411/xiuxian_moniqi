# Generated by Django 4.2.5 on 2023-12-28 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_clan", "0001_initial"),
        ("app_user", "0004_money_equipped"),
    ]

    operations = [
        migrations.AddField(
            model_name="characters",
            name="clan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Characters_clan",
                to="app_clan.clan",
            ),
        ),
    ]