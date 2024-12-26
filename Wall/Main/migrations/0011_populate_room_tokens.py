# Generated by Django 5.1.4 on 2024-12-26 15:00
from django.db import migrations
import Main.models

def populate_room_tokens(apps, schema_editor):
    Room = apps.get_model('Main', 'Room')
    for room in Room.objects.all():
        if not room.token:
            room.token = Main.models.generate_unique_token()
            room.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_room_token'),
    ]

    operations = [
        migrations.RunPython(populate_room_tokens),
    ]
