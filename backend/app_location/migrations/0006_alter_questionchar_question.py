# Generated by Django 4.1.3 on 2024-03-30 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0005_question_questionchar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionchar',
            name='question',
            field=models.IntegerField(default=0),
        ),
    ]
