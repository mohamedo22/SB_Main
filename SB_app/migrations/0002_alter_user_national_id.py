# Generated by Django 5.0.6 on 2024-05-25 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SB_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
