from django.urls import path
from . import views

urlpatterns = [
    path('', views.labtest_list, name='labtest_list'),
    path('add/', views.labtest_add, name='labtest_add'),
    path('edit/<int:pk>/', views.labtest_edit, name='labtest_edit'),
    path('details/<int:pk>/', views.labtest_details, name='labtest_details'),
    path('delete/<int:pk>/', views.labtest_delete, name='labtest_delete'),
]