from rest_framework import serializers
from .models import Product, Vitamins, Minerals, UserProfile, FoodConsumption
import datetime

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserProfileSerializer( serializers.ModelSerializer):
    calories_consumed_on_date = serializers.SerializerMethodField()

    #calories_left = serializers.SerializerMethodField()

    def get_calories_consumed_on_date(self, obj):
        return obj.calories_consumed_on_date

    def get_calories_left(self, obj):
        return obj.calories_left
    
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
            'weight_loss_pace',
            'calories_consumed_on_date',
            'date',
            'calories_left',
            'email',
        ]

    

    
class FoodConsumptionSerializer(serializers.ModelSerializer):
    #user_profile = UserProfileSerializer(source='user.userprofile', read_only=True)

    #user = UserProfileSerializer(many=False)
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
        ]

    def get_product_name(self, obj):
        return obj.product.name
    
    def get_consumed_kcal(self, obj):
        return obj.consumed_kcal
    

    
        