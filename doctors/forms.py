from django import forms
from .models import Doctor
from django.contrib.auth.models import User

class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField(required=False)

    class Meta:
        model = Doctor
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'address', 'photo',
            'specialization', 'qualification', 'experience',
            'consultation_fee', 'available_from', 'available_to', 'is_active'
        ]


