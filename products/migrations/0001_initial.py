# Generated by Django 4.2.11 on 2024-04-10 17:24

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('carbohydrates', models.FloatField()),
                ('fats', models.FloatField()),
                ('proteins', models.FloatField()),
                ('fibre', models.FloatField()),
                ('alcohol', models.FloatField(blank=True, null=True)),
                ('created_by', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vitamins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vitamin_A', models.FloatField(blank=True, null=True)),
                ('vitamin_B1', models.FloatField(blank=True, null=True)),
                ('vitamin_B2', models.FloatField(blank=True, null=True)),
                ('vitamin_B3', models.FloatField(blank=True, null=True)),
                ('vitamin_B5', models.FloatField(blank=True, null=True)),
                ('vitamin_B6', models.FloatField(blank=True, null=True)),
                ('vitamin_B12', models.FloatField(blank=True, null=True)),
                ('biotin', models.FloatField(blank=True, null=True)),
                ('vitamin_C', models.FloatField(blank=True, null=True)),
                ('choline', models.FloatField(blank=True, null=True)),
                ('vitamin_D', models.FloatField(blank=True, null=True)),
                ('vitamin_E', models.FloatField(blank=True, null=True)),
                ('vitamin_B9', models.FloatField(blank=True, null=True)),
                ('vitamin_K', models.FloatField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('activity_level', models.FloatField(choices=[(1.2, 'Sedentary (little to no exercise)'), (1.375, 'Lightly active (light exercise/sports 1-3 days/week)'), (1.55, 'Moderately active (moderate exercise/sports 3-5 days/week)'), (1.725, 'Very active (hard exercise/sports 6-7 days a week)'), (1.9, 'Extra active (very hard exercise/sports & physical job)')])),
                ('weight_goal', models.CharField(choices=[('lose', 'Lose'), ('maintain', 'Maintain'), ('gain', 'Gain')], max_length=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Minerals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calcium', models.FloatField(blank=True, null=True)),
                ('chloride', models.FloatField(blank=True, null=True)),
                ('chromium', models.FloatField(blank=True, null=True)),
                ('copper', models.FloatField(blank=True, null=True)),
                ('fluoride', models.FloatField(blank=True, null=True)),
                ('iodine', models.FloatField(blank=True, null=True)),
                ('iron', models.FloatField(blank=True, null=True)),
                ('magnesium', models.FloatField(blank=True, null=True)),
                ('manganese', models.FloatField(blank=True, null=True)),
                ('molybdenum', models.FloatField(blank=True, null=True)),
                ('potassium', models.FloatField(blank=True, null=True)),
                ('phosphorus', models.FloatField(blank=True, null=True)),
                ('selenium', models.FloatField(blank=True, null=True)),
                ('sodium', models.FloatField(blank=True, null=True)),
                ('sulfur', models.FloatField(blank=True, null=True)),
                ('zinc', models.FloatField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='FoodConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_consumed', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_consumed', models.DateField(default=datetime.datetime.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
