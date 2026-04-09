from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Patient
from .forms import PatientForm

User = get_user_model()

# Add patient
def patient_add(request):
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.pop('first_name')
            last_name = form.cleaned_data.pop('last_name')

            # Create unique username
            username = f"{first_name.lower()}.{last_name.lower()}"
            counter = 1
            orig_username = username
            while User.objects.filter(username=username).exists():
                username = f"{orig_username}{counter}"
                counter += 1

            user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            messages.success(request, "Patient added successfully!")
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, "patients/patient_add.html", {"form": form})

# List patients
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, "patients/patient_list.html", {"patients": patients})

# Edit patient
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    form.fields['first_name'].initial = patient.user.first_name
    form.fields['last_name'].initial = patient.user.last_name

    if request.method == "POST" and form.is_valid():
        patient.user.first_name = form.cleaned_data['first_name']
        patient.user.last_name = form.cleaned_data['last_name']
        patient.user.save()
        form.save()
        messages.success(request, "Patient updated successfully!")
        return redirect('patient_list')
    return render(request, "patients/patient_add.html", {"form": form})

# Delete patient
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.user.delete()  # also deletes patient due to OneToOne
    messages.success(request, "Patient deleted successfully!")
    return redirect('patient_list')

# Patient detail
def patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "patients/patient_view.html", {"patient": patient})