from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=150)
    generic_name = models.CharField(max_length=150, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    category = models.CharField(max_length=100, blank=True, null=True)  # Tablet, Syrup, etc.
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField()

    supplier = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()

    def __str__(self):
        return self.name
    

class Pharmacy(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=150, blank=True, null=True)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)

    license_number = models.CharField(max_length=100, blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)

    logo = models.ImageField(upload_to='pharmacy/logo/', blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name