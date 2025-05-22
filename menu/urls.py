from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),  # POST có table_id trong form
    path('cart/<str:table_id>/', views.view_cart, name='view_cart'),
    path('cart/<str:table_id>/remove/<str:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/<str:table_id>/place/', views.place_order, name='place_order'),
]