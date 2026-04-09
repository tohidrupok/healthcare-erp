from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('doctor-add/', views.doctor_add, name='doctor_add'),
    path('doctor-edit/<int:pk>/', views.doctor_edit, name='doctor_edit'),
    path('doctor-details/<int:pk>/', views.doctor_details, name='doctor_details'),
    path('doctor-delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),
    path('doctor-panel', views.doctor_consultation_panel, name='doctor_consultation_panel'),
    path('doctor-panel/<int:patient_id>/', views.doctor_consultation_panel, name='doctor_consultation_panel'),
    path('save-consultation/', views.save_consultation, name='save_consultation'),
]