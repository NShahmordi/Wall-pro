# Generated by Django 5.1.4 on 2024-12-26 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_alter_room_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='room',
        ),
    ]
