from django.shortcuts import render
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_list_view = ProductListAPIView.as_view()

class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

profile_view = UserProfileAPIView.as_view()