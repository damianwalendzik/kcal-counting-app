from django import forms

from .models import Product, FoodConsumption, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'carbohydrates',
            'fats',
            'proteins',
            'fibre',
            'alcohol',
            'total_kcal',
        ]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'gender',
            'weight',
            'height',
            'age',
            'activity_level',
            'weight_goal',
            'weight_loss_pace',
            'email',
        ]