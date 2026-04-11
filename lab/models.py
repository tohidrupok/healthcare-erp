from django.db import models

# 🔬 Lab Test Master
class LabTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    report_format = models.TextField(
        blank=True,
        help_text="Default report template"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
