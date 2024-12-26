# Generated by Django 5.1.4 on 2024-12-26 14:54

import Main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_advertisement_shirt_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='token',
            field=models.CharField(default=Main.models.generate_unique_token, max_length=36, unique=True),
        ),
    ]
