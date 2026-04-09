from django.db import models
from django.conf import settings  # ✅ correct

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Add explicit name fields
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='patients_photos/', null=True, blank=True)  # optional photo field

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"