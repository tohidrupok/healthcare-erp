from django import forms
from .models import LabTest,TestType,LabTestRequest

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = '__all__'
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),
        }



class TestTypeForm(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ['name', 'price', 'status'] # Explicitly naming fields is better practice
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., Blood Routine Test'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }



class LabTestRequestForm(forms.ModelForm):
    class Meta:
        model = LabTestRequest
        fields = ['patient', 'test_type', 'status']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Patient'
            }),
            'test_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(LabTestRequestForm, self). __init__(*args, **kwargs)