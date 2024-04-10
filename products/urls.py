from django.contrib import admin
from django.urls import path
from .views import product_list_view, profile_view
urlpatterns = [
    path('', product_list_view),
    path('profile/<int:pk>', profile_view)
]