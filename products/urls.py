from django.contrib import admin
from django.urls import path
from .views import product_API_view, profile_view, daily_consumption_view
urlpatterns = [
    path('products/', product_API_view),
    path('products/<int:pk>/', product_API_view),
    path('profile/<str:username>/', profile_view),
    path('profile/<str:username>/food_consumption/',daily_consumption_view),
    path('profile/<str:username>/food_consumption/<str:date>/',daily_consumption_view),

]