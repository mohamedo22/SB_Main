# Generated by Django 5.0.6 on 2024-05-25 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SB_app', '0002_alter_user_national_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
    ]
