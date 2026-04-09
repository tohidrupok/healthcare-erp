from django.db import models
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor


class Prescription(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)

    # Make these nullable for existing rows
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    medicines = models.TextField()
    dosage = models.TextField()
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Prescription'} - {self.patient}"