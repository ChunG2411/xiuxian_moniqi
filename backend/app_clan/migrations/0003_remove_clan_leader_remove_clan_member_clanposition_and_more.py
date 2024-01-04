# Generated by Django 4.2.5 on 2023-12-28 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_user", "0006_remove_characters_clan"),
        ("app_clan", "0002_clan_leader_remove_clan_member_clan_member"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clan",
            name="leader",
        ),
        migrations.RemoveField(
            model_name="clan",
            name="member",
        ),
        migrations.CreateModel(
            name="ClanPosition",
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
                    "position",
                    models.CharField(
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
                        max_length=10,
                    ),
                ),
                (
                    "char",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ClanPosition_char",
                        to="app_user.characters",
                    ),
                ),
                (
                    "clan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ClanPosition_clan",
                        to="app_clan.clan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Chức vị môn phái",
                "db_table": "tb_clan_position",
            },
        ),
        migrations.AddField(
            model_name="clan",
            name="member",
            field=models.IntegerField(default=0),
        ),
    ]
