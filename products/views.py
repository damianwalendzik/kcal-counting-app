from django.shortcuts import render
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime

class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        else:
            posts = self.get_queryset()
            serializer = self.get_serializer(posts, many=True)
            print(serializer.data)
            return Response(serializer.data)


product_API_view = ProductAPIView.as_view()

class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            product = self.get_object()
            serializer = self.get_serializer(product)
            return Response(serializer.data)

profile_view = UserProfileAPIView.as_view()

class DailyFoodConsumptionListView(generics.ListAPIView):
    queryset = FoodConsumption.objects.filter(date_consumed=datetime.today().date())
    serializer_class = FoodConsumptionSerializer

daily_consumption_view = DailyFoodConsumptionListView.as_view()