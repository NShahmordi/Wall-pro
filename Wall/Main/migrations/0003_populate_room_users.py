from django.db import migrations
from django.conf import settings

def populate_room_users(apps, schema_editor):
    Room = apps.get_model('Main', 'Room')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    for room in Room.objects.all():
        # Set default users or logic to determine user1 and user2
        room.user1 = User.objects.first()  # Example: setting the first user as user1
        room.user2 = User.objects.last()   # Example: setting the last user as user2
        room.save()

class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_add_field_user1_add_field_user2'),
    ]

    operations = [
        migrations.RunPython(populate_room_users),
    ]