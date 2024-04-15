from django.shortcuts import render, get_object_or_404
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User


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
    lookup_field='username'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        queryset = UserProfile.objects.filter(user__username=username)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

profile_view = UserProfileAPIView.as_view()

class DailyFoodConsumptionListView(generics.ListAPIView):

    queryset = FoodConsumption.objects.all()
    serializer_class = FoodConsumptionSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        date_str = kwargs.get('date')
        user = get_object_or_404(User, username=username)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        UserProfile.objects.update(date=date)
        queryset = FoodConsumption.objects.filter(user=user, date_consumed=date)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


daily_consumption_view = DailyFoodConsumptionListView.as_view()