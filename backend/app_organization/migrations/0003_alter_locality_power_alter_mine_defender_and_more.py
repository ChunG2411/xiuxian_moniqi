# Generated by Django 5.0.4 on 2024-05-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_organization', '0002_remove_locality_resources_market_mine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='power',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='mine',
            name='defender',
            field=models.IntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='mine',
            name='produce',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='mine',
            name='store',
            field=models.IntegerField(default=200),
        ),
    ]
