# Generated by Django 5.1.4 on 2024-12-25 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_advertisementimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='advertisement',
            name='Main_advert_title_1cfba0_idx',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='image',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='shirt_size',
        ),
        migrations.RemoveField(
            model_name='advertisementimage',
            name='uploaded_at',
        ),
    ]
