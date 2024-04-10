from rest_framework import serializers
from .models import Product, Vitamins, Minerals, UserProfile
import datetime

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.carbohydrates = validated_data.get('carbohydrates', instance.carbohydrates)
        instance.fats = validated_data.get('fats', instance.fats)
        instance.proteins = validated_data.get('proteins', instance.proteins)
        instance.fibre = validated_data.get('fibre', instance.fibre)
        instance.alcohol = validated_data.get('alcohol', instance.alcohol)

class UserProfileSerializer( serializers.ModelSerializer):
    class Meta:
        model = UserProfile

        fields = [
            'user',
            'gender',
            'weight',
            'height',
            'age',
            'activity_level',
            'weight_goal',
            'daily_kcal_requirement',
        ]

class FoodConsumptionSerializer( serializers.ModelSerializer):
    class Meta:
        fields = [
            'user',
            'product',
            'amount_consumed',
            'timestamp',
            'date_consumed',
            'consumed_kcal',
            'calories_consumed_on_date',
            'calories_left',
        ]