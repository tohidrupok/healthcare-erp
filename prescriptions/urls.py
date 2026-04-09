from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),
    path('add/', views.prescription_add, name='prescription_add'),
    path('edit/', views.prescription_edit, name='edit_prescription'),
    path('details/<int:pk>/', views.prescription_details, name='prescription_details'),
    path('delete/<int:pk>/', views.prescription_delete, name='prescription_delete'),
]