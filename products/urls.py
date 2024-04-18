from django.urls import path
from .views import index, product_list_API_view, profile_view, daily_consumption_list_create_view, retrieve_update_destroy_product_view        
urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list_API_view),
    path('products/<int:pk>/', retrieve_update_destroy_product_view),
    path('products/<int:pk>/delete/', retrieve_update_destroy_product_view),
    path('products/<int:pk>/update/', retrieve_update_destroy_product_view),
    path('profile/<str:user>/', profile_view),
    #path('profile/<str:username>/food_consumption/',daily_consumption_list_create_view),
    path('profile/<str:username>/food_consumption/<str:date>/',daily_consumption_list_create_view),

]