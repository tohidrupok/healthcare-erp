from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LabTest
from .forms import LabTestForm
from patients.models import Patient
from doctors.models import Doctor

@login_required
def labtest_list(request):
    tests = LabTest.objects.select_related('patient', 'doctor').order_by('-test_date')
    return render(request, "lab_tests/labtest_list.html", {"tests": tests})

@login_required
def labtest_add(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    if request.method == "POST":
        form = LabTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('labtest_list')
    else:
        form = LabTestForm()
    return render(request, "lab_tests/labtest_add.html", {
        "form": form,
        "doctors": doctors,
        "patients": patients
    })

@login_required
def labtest_edit(request, pk):    
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    test = get_object_or_404(LabTest, pk=pk)
    if request.method == "POST":
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('labtest_list')
    else:
        form = LabTestForm(instance=test)
    return render(request, "lab_tests/labtest_add.html", {
        "form": form,
        "test": test,
        "doctors": doctors,
        "patients": patients
    })



@login_required
def labtest_details(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    return render(request, "lab_tests/labtest_details.html", {"test": test})

@login_required
def labtest_delete(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    if request.method == "POST":
        test.delete()
        return redirect('labtest_list')
    return render(request, "lab_tests/labtest_delete.html", {"test": test})




