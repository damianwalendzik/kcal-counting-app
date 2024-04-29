from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Product, FoodConsumption, UserProfile

class CreateUserForm(UserCreationForm):
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES)
    weight = forms.FloatField()
    height = forms.FloatField()
    age = forms.IntegerField()
    activity_level = forms.ChoiceField(choices=UserProfile.ACTIVITY_LEVEL_CHOICES)
    weight_goal = forms.ChoiceField(choices=UserProfile.WEIGHT_GOAL_CHOICES)
    weight_loss_pace = forms.ChoiceField(choices=UserProfile.WEIGHT_CHANGE_PACE_CHOICES)

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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                gender=self.cleaned_data['gender'],
                weight=self.cleaned_data['weight'],
                height=self.cleaned_data['height'],
                age=self.cleaned_data['age'],
                activity_level=self.cleaned_data['activity_level'],
                weight_goal=self.cleaned_data['weight_goal'],
                weight_loss_pace=self.cleaned_data['weight_loss_pace'],
                email=self.cleaned_data['email'], # Added email field
            )
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

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
