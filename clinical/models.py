from django.db import models
from django.conf import settings
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from lab.models import LabTest



# 🧾 Prescription (Doctor creates)
class Prescription(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescription'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title or 'Prescription'} - {self.patient}"



# 💊 Prescription Medicine Items
class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items'
    )

    medicine = models.ForeignKey(
        'pharmacy.Medicine',
        on_delete=models.CASCADE
    )

    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine} ({self.dosage})"


# 🔥 LAB TEST PROCESS MODEL (FULL POWER MODEL)
class PrescriptionTest(models.Model):

    # priority system
    PRIORITY_CHOICES = [
        ('NORMAL', 'Normal'),
        ('URGENT', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DONE', 'Done'),
    ]

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='tests'
    )

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='NORMAL'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    # 👨‍🔬 who processed this test
    lab_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_tests'
    )

    # 📊 result data
    result = models.TextField(blank=True, null=True)

    report_file = models.FileField(
        upload_to='lab_reports/',
        blank=True,
        null=True
    )

    # 📏 medical reference range
    reference_range = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="e.g. 70-110 mg/dL"
    )

    performed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_test.name} - {self.prescription.patient}"