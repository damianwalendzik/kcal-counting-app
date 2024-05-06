from django.urls import path
from .views import index, dashboard,search_product, search_product_autocomplete_endpoint, my_login, register, user_logout, food_consumption_update_destroy_view, food_consumption_create_view, update_delete_profile_API_view, product_list_API_view, profile_view, daily_consumption_list_view, retrieve_update_destroy_product_view        
urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list_API_view),
    path('products/<int:pk>/', retrieve_update_destroy_product_view),
    path('products/<int:pk>/delete/', retrieve_update_destroy_product_view),
    path('products/<int:pk>/update/', retrieve_update_destroy_product_view),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('profile/<str:username>/editprofile/', update_delete_profile_API_view, name='edit_profile'),
    path('profile/<str:username>/food_consumption/search/autocomplete', search_product_autocomplete_endpoint, name='product-autocomplete'),
    path('profile/<str:username>/food_consumption/search/', search_product, name='search_product'),

    #path('profile/<str:username>/food_consumption/',daily_consumption_list_create_view),
    path('profile/<str:username>/food_consumption/<str:date>/',daily_consumption_list_view, name="consumption_view"),
    path('profile/<str:username>/food_consumption/<str:date>/<int:pk>/',food_consumption_update_destroy_view, name='update-meal'),
    path('profile/<str:username>/food_consumption/<str:date>/<int:pk>/delete/',food_consumption_update_destroy_view, name='delete-meal'),
    path('register/', register, name="register"),
    path('my-login/', my_login, name="my-login"),
    path('user-logout', user_logout, name='logout'),
    path('profile/<str:username>/dashboard/', dashboard, name='dashboard'),
]