from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_add, name='patient_add'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),
    path('view/<int:pk>/', views.patient_view, name='patient_view'),
]
