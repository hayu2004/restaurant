from django.urls import path
from . import views


urlpatterns = [
    path('', views.table_list, name='tables'),
    path('book/', views.table_order, name = 'table_order'),  # POST có table_id trong form
    path('success/', views.success, name = 'success'),
    path('failure/', views.failed, name = 'failure'),
    path('cancel_booking/', views.cancel_booking, name = 'cancel')
]

