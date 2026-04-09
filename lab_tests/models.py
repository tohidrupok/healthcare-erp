from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
from patients.models import Patient

class LabTest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=200)
    test_date = models.DateField()
    result = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return f"{self.test_name} - {self.patient}"
    


class TestType(models.Model):
    # Define choices for the status dropdown
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active'
    )

    def __str__(self):
        return self.name
    


class LabTestRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_requests')
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    
    # USE A STRING INSTEAD OF THE CLASS NAME:
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')