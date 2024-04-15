# Generated by Django 4.2.11 on 2024-04-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_userprofile_weight_loss_pace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='weight_loss_pace',
            field=models.FloatField(choices=[(-1.0, '-1.0'), (-0.9, '-0.9'), (-0.8, '-0.8'), (-0.7, '-0.7'), (-0.6, '-0.6'), (-0.5, '-0.5'), (-0.4, '-0.4'), (-0.3, '-0.3'), (-0.2, '-0.2'), (-0.1, '-0.1'), (0.0, '0.0'), (0.1, '0.1'), (0.2, '0.2'), (0.3, '0.3'), (0.4, '0.4'), (0.5, '0.5'), (0.6, '0.6'), (0.7, '0.7'), (0.8, '0.8'), (0.9, '0.9'), (1.0, '1.0')], default=0),
        ),
    ]
