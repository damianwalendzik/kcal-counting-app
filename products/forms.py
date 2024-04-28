from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Product, FoodConsumption, UserProfile

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2',
            ]

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


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

class FoodConsumptionForm(forms.ModelForm):
    class Meta:
        model = FoodConsumption
        fields = [
            'product',
            'amount_consumed',
        ]

class FoodEditForm(forms.ModelForm):
    class Meta:
        model = FoodConsumption
        fields = [
            'amount_consumed',
        ]
