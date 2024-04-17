from django.shortcuts import render, get_object_or_404
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        print(serializer.data)
        return Response(serializer.data)


product_list_API_view = ProductListAPIView.as_view()

class RetrieveUpdateDestroyProductAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
retrieve_update_destroy_product_view = RetrieveUpdateDestroyProductAPIView.as_view()

from rest_framework import status

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('user')
        queryset = UserProfile.objects.filter(user__username=username)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        username = kwargs.get('user')
        profile = UserProfile.objects.filter(user__username=username).first()
        if not profile:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the existing values for weight, height, and age from the database
        weight = profile.weight
        height = profile.height
        age = profile.age
        
        # Merge the existing values with the request data
        data = request.data.copy()
        data.update({'weight': weight, 'height': height, 'age': age})
        
        serializer = self.get_serializer(profile, data=data, partial=True)  # Use partial=True to allow partial updates
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        
        return Response(serializer.data)

profile_view = UserProfileAPIView.as_view()

class FoodConsumptionListAPIView(generics.ListAPIView):

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


daily_consumption_list_create_view = FoodConsumptionListAPIView.as_view()

