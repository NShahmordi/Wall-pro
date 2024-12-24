from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_populate_room_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_as_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]