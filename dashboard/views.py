from django.shortcuts import render
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

def dashboard_home(request):
    context = {
        "doctors_count": Doctor.objects.count(),
        "patients_count": Patient.objects.count(),
        "appointments_count": Appointment.objects.count(),
    }
    return render(request, "dashboard/home.html", context)