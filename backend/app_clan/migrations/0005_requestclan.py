# Generated by Django 4.2.5 on 2023-12-28 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_user", "0006_remove_characters_clan"),
        ("app_clan", "0004_alter_clan_member"),
    ]

    operations = [
        migrations.CreateModel(
            name="RequestClan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "char",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="RequestClan_char",
                        to="app_user.characters",
                    ),
                ),
                (
                    "clan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="RequestClan_clan",
                        to="app_clan.clan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Yêu cầu gia nhập",
                "db_table": "tb_request_clan",
            },
        ),
    ]
