from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, UserProfile, FoodConsumption
from .serializers import ProductSerializer, UserProfileSerializer, FoodConsumptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import UserProfileForm, FoodConsumptionForm, FoodEditForm, CreateUserForm, LoginForm
from django.utils import timezone
from django.contrib import auth
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')

    context = {'registerForm': form}
    return render(request, 'products/user-registration.html', context=context)


def my_login(request):
    if request.method == "POST":
        print('post method dziala')
        form = LoginForm(request.POST)  # Bind form to POST data
        print(form)
        print(form.errors)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            print(password)
            user = auth.authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print(user)
                print("post przeszlo i user nie jest none")
                auth.login(request, user)
                return redirect("profile_view")
    else:
        form = LoginForm()  # Initialize unbound form
        print(form.errors)
    context = {"loginform": form}
    return render(request, 'products/my-login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect("index")

def dashboard(request, username):
        profile = UserProfile.objects.filter(user=request.user)[0]
        kcal_requirement = profile.daily_kcal_requirement

        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now() + timedelta(days=30)
        date_list = []
        current_date = start_date
        while current_date <=end_date:
            date_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

        kcal_consumed_on_date = {}
        for dates in date_list:
            profile.date = dates
            kcal_consumed_on_date[dates]=profile.calories_consumed_on_date
        context = {'username': username,
                   'kcal_requirement': kcal_requirement,
                   'kcal_consumed_on_date': kcal_consumed_on_date
                   }
        return render(request, 'products/calendar.html', context=context)

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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
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


class UserProfileAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        queryset = UserProfile.objects.filter(user__username=username)
        serializer = self.get_serializer(queryset, many=True)
        user_profile_data = serializer.data[0]
        print(user_profile_data)
        del(user_profile_data['user'])
        del(user_profile_data['date'])
        del(user_profile_data['calories_left'])
        del(user_profile_data['calories_consumed_on_date'])

        context = {'user_profile': user_profile_data, 'username': username}
        return Response(context, template_name="products/profile.html", status=status.HTTP_200_OK)

profile_view = UserProfileAPIView.as_view()

class UpdateDeleteProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'  # Assuming 'user' is the field to look up the UserProfile
    queryset = UserProfile.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(UserProfile, user__username=username)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        form = UserProfileForm(instance=instance)
        return Response({'form': form}, template_name="products/editprofile.html")

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return Response({'success': True}, template_name="products/success.html")

update_delete_profile_API_view = UpdateDeleteProfileAPIView.as_view()


class FoodConsumptionListAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FoodConsumption.objects.all()
    serializer_class = FoodConsumptionSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/addmeal.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        date_str = kwargs.get('date')
        date = parse_date(date_str)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        
        form = FoodConsumptionForm(initial={
            'user': self.request.user, 
            'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S"), 
            'date_consumed': date
        })
        context = {'form': form, 'username': username, 'date': date}
        return render(request, 'products/addmeal.html', context)

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
            return HttpResponse('<h1>Success</h1>')
        else:
            return HttpResponse('<h1>Error: Form data is not valid</h1>', status=400)

food_consumption_create_view = FoodConsumptionCreateAPIView.as_view()

class FoodConsumptionUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
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


@login_required
def search_product(request, username):
    return render(request, 'products/search-product.html')

# @login_required
# def search_product_autocomplete_endpoint(request, username):
#     query = request.GET.get('query', '')
#     results = []
#     if query:
#         products = Product.objects.filter(name__icontains=query)[:5]
#         results = [product.name for product in products]

#     return JsonResponse({'results': results})
def search_product_autocomplete_endpoint(request, username):
    return JsonResponse({'data': 1})