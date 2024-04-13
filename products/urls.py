from django.contrib import admin
from django.urls import path
from .views import product_API_view, profile_view, daily_consumption_view
urlpatterns = [
    path('products/', product_API_view),
    path('profile/<int:pk>', profile_view),
    path('profile/food_consumption',daily_consumption_view),
]