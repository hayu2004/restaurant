from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.table_order, name='customer')
]

