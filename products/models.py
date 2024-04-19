from django.db import models
from django.conf import settings
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.apps import apps
from django.db.models import ExpressionWrapper, F, FloatField, Sum

User = settings.AUTH_USER_MODEL
###HOW TO ASSIGN USER TO MODEL:
#from django.apps import apps
#apps.get_models()
#Search for app with User
#apps.get_models()[<key>]

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    WEIGHT_GOAL_CHOICES = [
        ('lose', 'Lose'),
        ('maintain', 'Maintain'),
        ('gain', 'Gain')
    ]
    ACTIVITY_LEVEL_CHOICES = [
        (1.2, 'Sedentary (little to no exercise)'),
        (1.375, 'Lightly active (light exercise/sports 1-3 days/week)'),
        (1.55, 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        (1.725, 'Very active (hard exercise/sports 6-7 days a week)'),
        (1.9, 'Extra active (very hard exercise/sports & physical job)')
    ]
    WEIGHT_CHANGE_PACE_CHOICES = [
        (-1.0, '-1.0'), (-0.9, '-0.9'), (-0.8, '-0.8'), 
        (-0.7, '-0.7'), (-0.6, '-0.6'), (-0.5, '-0.5'), 
        (-0.4, '-0.4'), (-0.3, '-0.3'), (-0.2, '-0.2'), 
        (-0.1, '-0.1'), (0.0, '0.0'), (0.1, '0.1'), 
        (0.2, '0.2'), (0.3, '0.3'), (0.4, '0.4'), 
        (0.5, '0.5'), (0.6, '0.6'), (0.7, '0.7'), 
        (0.8, '0.8'), (0.9, '0.9'), (1.0, '1.0'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    activity_level = models.FloatField(choices=ACTIVITY_LEVEL_CHOICES)
    weight_goal = models.CharField(choices=WEIGHT_GOAL_CHOICES, max_length=8)
    weight_loss_pace = models.FloatField(choices=WEIGHT_CHANGE_PACE_CHOICES, default=0)
    date=models.DateField(default=datetime.now)
    email=models.EmailField()

    def __str__(self):
        return self.user.username

    @property
    def daily_kcal_requirement(self):
        if self.weight_goal == "lose":
            goal_multiplier = 0.8
        elif self.weight_goal == "maintain":
            goal_multiplier = 1
        else:
            goal_multiplier = 1.2

        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        if self.gender == 'female':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        kcal_requirement = bmr * goal_multiplier * self.activity_level
        return kcal_requirement
    
    @property
    def calories_consumed_on_date(self):
        consumed_kcal = FoodConsumption.objects.filter(user=self.user, date_consumed=self.date).aggregate(
            total=Sum(ExpressionWrapper(F('product__total_kcal') * F('amount_consumed')/100,output_field=FloatField())))['total'] or 0
        return consumed_kcal


    def calories_left(self):
        calories_left = self.daily_kcal_requirement - self.calories_consumed_on_date
        return calories_left

    
class Product(models.Model):
    '''
    All macros and micros have to be scaled to 100g of given Product.
    '''
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    proteins = models.FloatField()
    fibre = models.FloatField()
    alcohol = models.FloatField(null=True, blank=True)
    total_kcal = models.FloatField() # 4*(proteins + carbohydrates) + 7*alcohol + 9*fats
    
    def __str__(self):
        return self.name


class FoodConsumption(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_consumed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    date_consumed = models.DateField(default=datetime.now)

    @property
    def consumed_kcal(self):
        return self.product.total_kcal * self.amount_consumed / 100
    

class Vitamins(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vitamin_A = models.FloatField(null=True, blank=True) #Retinoids and Carothene
    vitamin_B1 = models.FloatField(null=True, blank=True) #Thiamin
    vitamin_B2 = models.FloatField(null=True, blank=True) #Riboflavin
    vitamin_B3 = models.FloatField(null=True, blank=True) #Niacin
    vitamin_B5 = models.FloatField(null=True, blank=True) #Panthothenic Acid
    vitamin_B6 = models.FloatField(null=True, blank=True) #Pyridoxine
    vitamin_B12 = models.FloatField(null=True, blank=True) #Cobalamin
    biotin = models.FloatField(null=True, blank=True) #Biotin
    vitamin_C = models.FloatField(null=True, blank=True) #Ascorbic Acid
    choline = models.FloatField(null=True, blank=True) #Choline
    vitamin_D = models.FloatField(null=True, blank=True) #Calciferol
    vitamin_E = models.FloatField(null=True, blank=True) #Alpha Tocopherol
    vitamin_B9 = models.FloatField(null=True, blank=True) #folic acid
    vitamin_K = models.FloatField(null=True, blank=True) #Phylloquinone, Menadione

class Minerals(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    calcium = models.FloatField(null=True, blank=True) 
    chloride = models.FloatField(null=True, blank=True) 
    chromium = models.FloatField(null=True, blank=True) 
    copper = models.FloatField(null=True, blank=True) 
    fluoride = models.FloatField(null=True, blank=True) 
    iodine = models.FloatField(null=True, blank=True) 
    iron = models.FloatField(null=True, blank=True) 
    magnesium = models.FloatField(null=True, blank=True) 
    manganese = models.FloatField(null=True, blank=True) 
    molybdenum = models.FloatField(null=True, blank=True) 
    potassium = models.FloatField(null=True, blank=True) 
    phosphorus = models.FloatField(null=True, blank=True) 
    selenium = models.FloatField(null=True, blank=True) 
    sodium = models.FloatField(null=True, blank=True) 
    sulfur = models.FloatField(null=True, blank=True) 
    zinc = models.FloatField(null=True, blank=True) 