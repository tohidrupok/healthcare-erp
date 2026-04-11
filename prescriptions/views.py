from django.shortcuts import render, redirect, get_object_or_404
from .models import Prescription
from .forms import PrescriptionForm
from appointments.models import Appointment


def prescription_list(request):
    # Use select_related to avoid extra queries
    prescriptions = Prescription.objects.select_related(
        'appointment',  # appointment
        'appointment__doctor',  # doctor linked to appointment
        'appointment__patient',  # patient linked to appointment
        'doctor',  # doctor directly in prescription
        'patient'  # patient directly in prescription
    ).order_by('-created_at')

    # Pass prescriptions to template
    return render(request, "prescriptions/prescription_list.html", {
        "prescriptions": prescriptions
    })

# -----------------------------
# ADD NEW PRESCRIPTION
# -----------------------------
def prescription_add(request):
    appointments = Appointment.objects.all()

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            # Don't save yet
            prescription = form.save(commit=False)

            # Set doctor and patient based on the selected appointment
            prescription.doctor = prescription.appointment.doctor
            prescription.patient = prescription.appointment.patient

            prescription.save()
            return redirect('prescription_list')
        else:
            print(form.errors)  # DEBUG: shows form errors in console
    else:
        form = PrescriptionForm()

    return render(request, "prescriptions/prescription_add.html", {
        "form": form,
        "appointments": appointments,
        "action": "Add"
    })

# -----------------------------
# EDIT PRESCRIPTION
# -----------------------------
def prescription_edit(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    appointments = Appointment.objects.all()

    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, "prescriptions/prescription_add.html", {
        "form": form,
        "appointments": appointments,
        "action": "Edit",
        "prescription": prescription
    })

# -----------------------------
# PRESCRIPTION DETAILS VIEW
# -----------------------------
def prescription_details(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, "prescriptions/prescription_details.html", {
        "prescription": prescription
    })

# ---------------------------------
# DELETE PRESCRIPTION FROM DATABASE
# ---------------------------------
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)

    if request.method == "POST":
        prescription.delete()
        return redirect('prescription_list')

    return render(request, "prescriptions/prescription_delete.html", {
        "prescription": prescription
    })