from django.shortcuts import render, get_object_or_404
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
def index(request):

    return render(request, 'products/index.html', {
        'items':'Hello world'
    })
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
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('user')
        queryset = UserProfile.objects.filter(user__username=username)
        print(queryset[0].user)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data[0])
        print(serializer.data[0]['user'])
        user_profile_data = serializer.data[0]
        return Response({'user_profile': user_profile_data}, template_name="products/profile.html")

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/foodconsumption.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        date_str = kwargs.get('date')
        user = get_object_or_404(User, username=username)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        UserProfile.objects.update(date=date)
        queryset = FoodConsumption.objects.filter(user=user, date_consumed=date)
        serializer = self.get_serializer(queryset, many=True)
        food_consumption_data_list = serializer.data
        calories_eaten = UserProfile.objects.filter(user=user)[0].calories_consumed_on_date
        calories_left = UserProfile.objects.filter(user=user)[0].calories_left
        context = {'food_consumption_list': food_consumption_data_list, 
                   'user': user, 
                   'calories_eaten': calories_eaten,
                   'date': date,
                   'calories_left': calories_left
                   }

        return Response(context)


daily_consumption_list_create_view = FoodConsumptionListAPIView.as_view()

