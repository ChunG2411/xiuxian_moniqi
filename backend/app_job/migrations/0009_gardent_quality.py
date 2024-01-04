# Generated by Django 4.2.5 on 2023-12-29 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_job", "0008_remove_gardentslot_start_time_gardentslot_end_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="gardent",
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
    ]