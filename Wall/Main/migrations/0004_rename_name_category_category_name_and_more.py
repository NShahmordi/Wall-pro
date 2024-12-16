# Generated by Django 5.0 on 2024-12-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_room_alter_users_options_alter_users_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='name',
            new_name='city_name',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=50, unique=True, verbose_name='username'), max_length=200, unique=True),
        ),
    ]
