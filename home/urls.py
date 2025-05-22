from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('review/', views.review, name='review'),
    path('user/', views.user, name='user')
]