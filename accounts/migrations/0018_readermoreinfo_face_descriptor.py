# Generated by Django 5.0.5 on 2024-05-15 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='readermoreinfo',
            name='face_descriptor',
            field=models.TextField(blank=True, null=True),
        ),
    ]
