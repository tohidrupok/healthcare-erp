from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from doctors.models import Doctor
from patients.models import Patient

@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('doctor', 'patient').order_by('-appointment_date', '-appointment_time')
    return render(request, "appointments/appointment_list.html", {"appointments": appointments})

@login_required
def appointment_add(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, "appointments/appointment_add.html", {
        "form": form,
        "doctors": doctors,
        "patients": patients
    })

@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, "appointments/appointment_add.html", {
        "form": form,
        "appointment": appointment,
        "doctors": doctors,
        "patients": patients
    })



@login_required
def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, "appointments/appointment_details.html", {"appointment": appointment})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect('appointment_list')
    return render(request, "appointments/appointment_delete.html", {"appointment": appointment})



