from django import forms
from .models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'appointment',
            'title',
            'date',
            'status',
            'medicines',
            'dosage',
            'notes',
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'medicines': forms.Textarea(attrs={'rows': 3}),
            'dosage': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }