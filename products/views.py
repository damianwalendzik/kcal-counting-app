from django.shortcuts import render, get_object_or_404
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import UserProfileForm, FoodConsumptionForm, FoodEditForm
from django.utils import timezone
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

class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('user')
        queryset = UserProfile.objects.filter(user__username=username)
        serializer = self.get_serializer(queryset, many=True)
        user_profile_data = serializer.data[0]
        context = {'user_profile': user_profile_data, 'username': username}
        return Response(context, template_name="products/profile.html", status=status.HTTP_200_OK)

profile_view = UserProfileAPIView.as_view()

class UpdateDeleteProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'user'
    queryset = UserProfile.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('user')
        queryset = UserProfile.objects.filter(user__username=username)
        instance = get_object_or_404(queryset)
        print("INSTANCE")
        print(instance)
        form = UserProfileForm(instance=instance)
        return Response({'form': form}, template_name="products/editprofile.html")


    def post(self, request, *args, **kwargs):
        username = kwargs.get('user')
        queryset = UserProfile.objects.filter(user__username=username)
        instance = get_object_or_404(queryset)
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return Response({'success': True}, template_name="products/success.html")


update_delete_profile_API_view = UpdateDeleteProfileAPIView.as_view()

class FoodConsumptionListAPIView(generics.ListAPIView):

    queryset = FoodConsumption.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/foodconsumption.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        date_str = kwargs.get('date')
        pk = kwargs.get('pk')
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
                   'calories_left': calories_left,
                   'pk':pk,
                   }
        print(context)
        return Response(context)


daily_consumption_list_view = FoodConsumptionListAPIView.as_view()

class FoodConsumptionCreateAPIView(generics.CreateAPIView):
    queryset = FoodConsumption.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/addmeal.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        date_str = kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        form = FoodConsumptionForm(initial=
                                   {'user': self.request.user, 
                                    'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                    'date_consumed': date})
        return Response({'form': form, 'username': username, 'date': date}, template_name="products/addmeal.html")

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        date_str = kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        form = FoodConsumptionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.date_consumed = date
            instance.save()
            return Response({'success': True}, template_name="products/success.html")
        else:
            return Response({'error': 'Form data is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

food_consumption_create_view = FoodConsumptionCreateAPIView.as_view()


class FoodConsumptionUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodConsumption.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/addmeal.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        date_str = kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        pk = kwargs.get('pk')
        product = get_object_or_404(FoodConsumption, pk=pk).product
        form = FoodEditForm(initial=
                                   {'user': self.request.user, 
                                    'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                    'date_consumed': date,
                                    "pk": pk,
                                    'product': product})
        return Response({'form': form, 'username': username, 'date': date}, template_name="products/addmeal.html")

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        date_str = kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        pk = kwargs.get('pk')
        product = get_object_or_404(FoodConsumption, pk=pk).product

        # Retrieve the existing FoodConsumption instance from the database
        instance = self.get_object()
        print(instance)
        form = FoodEditForm(request.POST, instance=instance)  # Pass instance to update existing record
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.product = product
            instance.date_consumed = date
            instance.save()
            return Response({'success': True}, template_name="products/success.html")
        else:
            return Response({'error': 'Form data is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

food_consumption_update_destroy_view = FoodConsumptionUpdateDestroyAPIView.as_view()
