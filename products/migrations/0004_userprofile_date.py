# Generated by Django 4.2.11 on 2024-04-15 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_userprofile_weight_loss_pace'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
