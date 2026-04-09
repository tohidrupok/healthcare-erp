from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('lab-tests/', include('lab_tests.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)