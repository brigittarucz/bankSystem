# Generated by Django 3.1.6 on 2021-04-28 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210428_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='currency_timestamp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rate',
            name='rate_timestamp',
            field=models.IntegerField(default=0),
        ),
    ]
