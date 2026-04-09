from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_add, name='appointment_add'),
    path('edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('details/<int:pk>/', views.appointment_details, name='appointment_details'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
]