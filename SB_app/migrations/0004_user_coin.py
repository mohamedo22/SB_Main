# Generated by Django 5.0.6 on 2024-05-25 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SB_app', '0003_remove_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coin',
            field=models.CharField(default='Egypt', max_length=50),
        ),
    ]