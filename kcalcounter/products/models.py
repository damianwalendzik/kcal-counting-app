from django.db import models
from django.conf import settings
import datetime


User = settings.AUTH_USER_MODEL
class Product(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(datetime.datetime.now())
    carbohydrates = models.FloatField(max_length=5)
    fats = models.FloatField(max_length=5)
    proteins = models.FloatField(max_length=5)
    fibre = models.FloatField(max_length=5)
    alcohol = models.FloatField(max_length=5, null=True, blank=True)

class Vitamins(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vitamin_A = models.FloatField(max_length=10,  null=True, blank=True) #Retinoids and Carothene
    vitamin_B1 = models.FloatField(max_length=10,  null=True, blank=True) #Thiamin
    vitamin_B2 = models.FloatField(max_length=10,  null=True, blank=True) #Riboflavin
    vitamin_B3 = models.FloatField(max_length=10,  null=True, blank=True) #Niacin
    vitamin_B5 = models.FloatField(max_length=10,  null=True, blank=True) #Panthothenic Acid
    vitamin_B6 = models.FloatField(max_length=10,  null=True, blank=True) #Pyridoxine
    vitamin_B12 = models.FloatField(max_length=10,  null=True, blank=True) #Cobalamin
    biotin = models.FloatField(max_length=10,  null=True, blank=True) #Biotin
    vitamin_C = models.FloatField(max_length=10,  null=True, blank=True) #Ascorbic Acid
    choline = models.FloatField(max_length=10,  null=True, blank=True) #Choline
    vitamin_D = models.FloatField(max_length=10,  null=True, blank=True) #Calciferol
    vitamin_E = models.FloatField(max_length=10,  null=True, blank=True) #Alpha Tocopherol
    vitamin_B9 = models.FloatField(max_length=10,  null=True, blank=True) #folic acid
    vitamin_K = models.FloatField(max_length=10,  null=True, blank=True) #Phylloquinone, Menadione

class Minerals(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    calcium = models.FloatField(max_length=10,  null=True, blank=True) 
    chloride = models.FloatField(max_length=10,  null=True, blank=True) 
    chromium = models.FloatField(max_length=10,  null=True, blank=True) 
    copper = models.FloatField(max_length=10,  null=True, blank=True) 
    fluoride = models.FloatField(max_length=10,  null=True, blank=True) 
    iodine = models.FloatField(max_length=10,  null=True, blank=True) 
    iron = models.FloatField(max_length=10,  null=True, blank=True) 
    magnesium = models.FloatField(max_length=10,  null=True, blank=True) 
    manganese = models.FloatField(max_length=10,  null=True, blank=True) 
    molybdenum = models.FloatField(max_length=10,  null=True, blank=True) 
    potassium = models.FloatField(max_length=10,  null=True, blank=True) 
    phosphorus = models.FloatField(max_length=10,  null=True, blank=True) 
    selenium = models.FloatField(max_length=10,  null=True, blank=True) 
    sodium = models.FloatField(max_length=10,  null=True, blank=True) 
    sulfur = models.FloatField(max_length=10,  null=True, blank=True) 
    zinc = models.FloatField(max_length=10,  null=True, blank=True) 





