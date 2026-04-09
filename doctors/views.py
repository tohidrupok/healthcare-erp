from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor
from .forms import DoctorForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from patients.models import Patient
from prescriptions.models import Prescription
from lab_tests.models import LabTestRequest, TestType
from django.utils import timezone
from appointments.models import Appointment
from django.contrib import messages

User = get_user_model()

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create a unique username
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = f"{first_name.lower()}.{last_name.lower()}"
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1

                # Create user using custom user model
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password='defaultpassword123'
                )

                # Create Doctor instance
                doctor = Doctor(
                    user=user,
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    gender=form.cleaned_data['gender'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    specialization=form.cleaned_data['specialization'],
                    qualification=form.cleaned_data['qualification'],
                    experience=form.cleaned_data['experience'],
                    consultation_fee=form.cleaned_data['consultation_fee'],
                    available_from=form.cleaned_data['available_from'],
                    available_to=form.cleaned_data['available_to'],
                    is_active=form.cleaned_data['is_active']
                )

                if request.FILES.get('photo'):
                    doctor.photo = request.FILES['photo']

                doctor.save()
                messages.success(request, f"Doctor {user.get_full_name()} added successfully!")
                return redirect('doctor_list')

            except Exception as e:
                print("Error saving doctor:", e)
                messages.error(request, f"Error saving doctor: {e}")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Form is invalid! Check console for details.")
    else:
        form = DoctorForm()

    return render(request, 'doctors/doctor_add.html', {'form': form})



def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            # Update User fields
            doctor.user.first_name = form.cleaned_data['first_name']
            doctor.user.last_name = form.cleaned_data['last_name']
            doctor.user.save()
            form.save()
            return redirect('doctor_list')
    else:
        initial = {
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
            'date_of_birth': doctor.date_of_birth,
            'gender': doctor.gender,
            'phone': doctor.phone,
            'address': doctor.address,
        }
        form = DoctorForm(instance=doctor, initial=initial)
    return render(request, 'doctors/doctor_add.html', {'form': form})



def doctor_details(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_details.html', {'doctor': doctor})


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.user.delete()  # Also deletes related user
    doctor.delete()
    return redirect('doctor_list')



# def doctor_consultation_panel(request, patient_id=None):
#     context = {}
    
#     # 1. Fetch all patients for the sidebar 
#     # FIX: Changed 'name' to 'first_name' to avoid FieldError
#     context['patients'] = Patient.objects.all().order_by('first_name')
    
#     # 2. Fetch all available test types for the selection panel
#     context['test_types'] = TestType.objects.all()

#     # 3. If a specific patient is selected, load their data
#     if patient_id:
#         patient = get_object_or_404(Patient, id=patient_id)
#         context['selected_patient'] = patient
        
#         # LIFO History: Most recent visits first
#         context['history'] = Prescription.objects.filter(patient=patient).order_by('-created_at')
#         context['past_tests'] = LabTestRequest.objects.filter(patient=patient).order_by('-date_ordered')

#     # 4. Handle Saving the Consultation (POST)
#     if request.method == "POST":
#         # Get the patient from the hidden input in your form
#         post_patient_id = request.POST.get('patient_id')
#         if post_patient_id:
#             current_patient = get_object_or_404(Patient, id=post_patient_id)
            
#             # Save the Prescription
#             advice = request.POST.get('advice')
#             diagnosis = request.POST.get('complaints')
            
#             prescription = Prescription.objects.create(
#                 patient=current_patient,
#                 diagnosis=diagnosis,
#                 instructions=advice
#             )

#             # Save Selected Lab Tests
#             selected_test_ids = request.POST.getlist('tests') 
#             for test_id in selected_test_ids:
#                 test_type = get_object_or_404(TestType, id=test_id)
#                 LabTestRequest.objects.create(
#                     patient=current_patient,
#                     test_type=test_type,
#                     status='Pending'
#                 )
            
#             # FIX: Use first_name here or the @property name if you defined it
#             messages.success(request, f"Consultation for {current_patient.first_name} completed!")
#             return redirect('doctor_consultation_panel', patient_id=current_patient.id)

#     return render(request, 'doctors/consultation_panel.html', context)




# def doctor_consultation_panel(request, patient_id=None):
#     context = {}
    
#     # 1. Sidebar Patient List (Always available for searching)
#     # Ordered by first_name to fix the previous FieldError
#     context['patients'] = Patient.objects.all().order_by('first_name')
    
#     # 2. Lab Test Options (Available for the checkbox panel)
#     context['test_types'] = TestType.objects.all()

#     # 3. Handle specific patient selection
#     if patient_id:
#         selected_patient = get_object_or_404(Patient, id=patient_id)
#         context['selected_patient'] = selected_patient
        
#         # LIFO History: Most recent prescriptions at the top
#         # We use select_related or prefetch_related if you want to show tests inside history
#         context['history'] = Prescription.objects.filter(
#             patient=selected_patient
#         ).order_by('-created_at')
        
#         # Past Lab Tests LIFO
#         context['past_tests'] = LabTestRequest.objects.filter(
#             patient=selected_patient
#         ).order_by('-date_ordered')

#     # 4. Handle Saving the Consultation (POST)
#     if request.method == "POST":
#         post_patient_id = request.POST.get('patient_id')
        
#         if post_patient_id:
#             current_patient = get_object_or_404(Patient, id=post_patient_id)
            
#             # Extract data from form
#             advice = request.POST.get('advice')
#             diagnosis = request.POST.get('complaints')
            
#             # Create the Prescription record
#             prescription = Prescription.objects.create(
#                 patient=current_patient,
#                 diagnosis=diagnosis,
#                 instructions=advice
#             )

#             # Create Lab Test Requests from selected checkboxes
#             selected_test_ids = request.POST.getlist('tests') 
#             for test_id in selected_test_ids:
#                 test_obj = get_object_or_404(TestType, id=test_id)
#                 LabTestRequest.objects.create(
#                     patient=current_patient,
#                     test_type=test_obj,
#                     status='Pending'
#                 )
            
#             messages.success(request, f"Consultation for {current_patient.first_name} saved successfully!")
            
#             # Redirect back to the same patient to see updated LIFO history immediately
#             return redirect('doctor_consultation_panel', patient_id=current_patient.id)

#     return render(request, 'doctors/consultation_panel.html', context)



# def save_consultation(request):
#     if request.method == "POST":
#         p_id = request.POST.get('patient_id')
#         patient = get_object_or_404(Patient, id=p_id)
#         current_doctor = getattr(request.user, 'doctor', None)

#         # 1. Get the latest Appointment
#         appointment = Appointment.objects.filter(patient=patient).order_by('-created_at').first()
        
#         if not appointment:
#             messages.error(request, "No appointment found for this patient.")
#             return redirect('doctor_consultation_panel', patient_id=patient.id)

#         prescription, created = Prescription.objects.update_or_create(
#             appointment=appointment, # The unique lookup field
#             defaults={
#                 'patient': patient,
#                 'doctor': current_doctor,
#                 'title': f"Prescription - {timezone.now().date()}",
#                 'date': timezone.now().date(),
#                 'status': 'COMPLETED',
#                 'medicines': request.POST.get('advice'),
#                 'dosage': "As prescribed",
#                 'notes': request.POST.get('complaints'),
#             }
#         )

#         # 3. Lab Tests (Usually multiple tests are okay, so we keep creating them)
#         selected_tests = request.POST.getlist('tests')
#         for test_id in selected_tests:
#             test_type = get_object_or_404(TestType, id=test_id)
#             LabTestRequest.objects.create(
#                 patient=patient,
#                 doctor=current_doctor,
#                 test_type=test_type,
#                 status='Pending'
#             )
        
#         msg = "New record created!" if created else "Existing record updated!"
#         messages.success(request, f"Consultation for {patient.first_name} {msg}")
#         return redirect('doctor_consultation_panel', patient_id=patient.id)

#     return redirect('doctor_consultation_panel')



def doctor_consultation_panel(request, patient_id=None):
    context = {}
    
    # 1. Sidebar Patient List & Lab Test Options
    context['patients'] = Patient.objects.all().order_by('first_name')
    context['test_types'] = TestType.objects.filter(status='active')

    # 2. Handle specific patient selection
    if patient_id:
        selected_patient = get_object_or_404(Patient, id=patient_id)
        context['selected_patient'] = selected_patient
        
        # LIFO History using your actual model fields
        context['history'] = Prescription.objects.filter(
            patient=selected_patient
        ).order_by('-created_at')
        
        context['past_tests'] = LabTestRequest.objects.filter(
            patient=selected_patient
        ).order_by('-date_ordered')

    # 3. Handle Saving (POST)
    if request.method == "POST":
        post_patient_id = request.POST.get('patient_id')
        if post_patient_id:
            current_patient = get_object_or_404(Patient, id=post_patient_id)
            
            # Find the most recent appointment for this patient to satisfy the OneToOne requirement
            appointment = Appointment.objects.filter(patient=current_patient).order_by('-created_at').first()
            
            if not appointment:
                messages.error(request, "No appointment found for this patient. Cannot save prescription.")
                return redirect('doctor_consultation_panel', patient_id=current_patient.id)

            # Map form 'complaints' to model 'notes' and form 'advice' to model 'medicines'
            # Using update_or_create to avoid UNIQUE constraint error on Appointment
            Prescription.objects.update_or_create(
                appointment=appointment,
                defaults={
                    'patient': current_patient,
                    'doctor': getattr(request.user, 'doctor', None),
                    'notes': request.POST.get('complaints'),
                    'medicines': request.POST.get('advice'),
                    'dosage': "As directed", # Default value for model field
                    'date': timezone.now().date(),
                    'status': 'COMPLETED'
                }
            )

            # Save Lab Tests
            selected_test_ids = request.POST.getlist('tests') 
            for test_id in selected_test_ids:
                test_obj = get_object_or_404(TestType, id=test_id)
                LabTestRequest.objects.create(
                    patient=current_patient,
                    doctor=getattr(request.user, 'doctor', None),
                    test_type=test_obj,
                    status='Pending'
                )
            
            messages.success(request, f"Record for {current_patient.first_name} updated successfully!")
            return redirect('doctor_consultation_panel', patient_id=current_patient.id)

    return render(request, 'doctors/consultation_panel.html', context)





# def save_consultation(request):
#     if request.method == "POST":
#         p_id = request.POST.get('patient_id')
#         patient = get_object_or_404(Patient, id=p_id)
#         current_doctor = getattr(request.user, 'doctor', None)
        
#         # 1. Get/Update the Prescription (Notes and Medicines)
#         appointment = Appointment.objects.filter(patient=patient).latest('created_at')
        
#         prescription, created = Prescription.objects.update_or_create(
#             appointment=appointment,
#             defaults={
#                 'patient': patient,
#                 'doctor': current_doctor,
#                 'notes': request.POST.get('complaints'), # Diagnosis
#                 'medicines': request.POST.get('advice'), # Prescription
#                 'status': 'COMPLETED',
#                 'date': timezone.now().date(),
#             }
#         )

#         # 2. Save Lab Tests to LabTestRequest table
#         selected_test_ids = request.POST.getlist('tests')
#         for t_id in selected_test_ids:
#             test_type = get_object_or_404(TestType, id=t_id)
#             LabTestRequest.objects.create(
#                 patient=patient,
#                 doctor=current_doctor,
#                 test_type=test_type,
#                 status='Pending'
#             )

#         messages.success(request, "Consultation and Lab Tests saved successfully!")
#         return redirect('doctor_consultation_panel', patient_id=patient.id)




def save_consultation(request):
    if request.method == "POST":
        p_id = request.POST.get('patient_id')
        patient = get_object_or_404(Patient, id=p_id)
        current_doctor = getattr(request.user, 'doctor', None)

        # ✅ SAFE: get latest appointment (no crash)
        appointment = Appointment.objects.filter(
            patient=patient
        ).order_by('-created_at').first()

        if not appointment:
            messages.error(request, "No appointment found for this patient.")
            return redirect('doctor_consultation_panel', patient_id=patient.id)

        # ✅ Save prescription (consultation history)
        prescription, created = Prescription.objects.update_or_create(
            appointment=appointment,
            defaults={
                'patient': patient,
                'doctor': current_doctor,
                'notes': request.POST.get('complaints'),
                'medicines': request.POST.get('advice'),
                'dosage': request.POST.get('advice'),  # optional mapping
                'status': 'COMPLETED',
                'date': timezone.now().date(),
                'title': f"Consultation - {timezone.now().strftime('%d %b %Y')}",
            }
        )

        # ✅ Save Lab Tests (NO duplicate)
        selected_test_ids = request.POST.getlist('tests')

        for t_id in selected_test_ids:
            test_type = get_object_or_404(TestType, id=t_id)

            LabTestRequest.objects.get_or_create(
                patient=patient,
                doctor=current_doctor,
                test_type=test_type,
                defaults={'status': 'Pending'}
            )

        messages.success(request, "Consultation and Lab Tests saved successfully!")
        return redirect('doctor_consultation_panel', patient_id=patient.id)