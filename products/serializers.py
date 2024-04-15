from rest_framework import serializers
from .models import Product, Vitamins, Minerals, UserProfile, FoodConsumption
import datetime

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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

class FoodConsumptionSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False)
    product_name = serializers.SerializerMethodField()
    consumed_kcal = serializers.SerializerMethodField()
    class Meta:
        model = FoodConsumption
        fields = [
            'user',
            'product',
            'product_name',
            'amount_consumed',
            'timestamp',
            'date_consumed',
            'consumed_kcal',
            #'calories_consumed_on_date',
            #'calories_left',
        ]

    def get_product_name(self, obj):
        return obj.product.name
    
    def get_consumed_kcal(self, obj):
        return obj.consumed_kcal
        