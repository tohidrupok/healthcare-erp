from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    available_from = models.TimeField()
    available_to = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"    

