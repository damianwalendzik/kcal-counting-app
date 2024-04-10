from rest_framework import serializers
from .models import Product, Vitamins, Minerals
import datetime

class ProductSerializer( serializers.ModelSerializer):
    class Meta:
        fields = [
            'name',
            'created_by',
            'timestamp',
            'carbohydrates',
            'fats',
            'proteins',
            'fibre',
            'alcohol',
            'kcal',

        ]
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


