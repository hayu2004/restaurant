from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.log_in),
    path('staff/staff_dashboard', views.staff_dashboard, name='table'),
    path('staff/staff_manager_dashboard', views.staff_manager_dashboard)
]