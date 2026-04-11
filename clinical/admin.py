from django.contrib import admin
from .models import Prescription, PrescriptionItem, PrescriptionTest


# 💊 Medicine Inline
class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


# 🔬 Lab Test Inline (NO autocomplete to avoid error)
class PrescriptionTestInline(admin.TabularInline):
    model = PrescriptionTest
    extra = 1


# 🧾 Prescription Admin
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'status', 'date', 'created_at']
    list_filter = ['status', 'doctor', 'date']
    search_fields = ['id', 'patient__name', 'doctor__name']
    date_hierarchy = 'created_at'

    inlines = [PrescriptionItemInline, PrescriptionTestInline]


# 💊 Prescription Item Admin
@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'prescription', 'medicine', 'dosage', 'duration']
    search_fields = ['medicine__name']


# 🔥 Lab Workflow Admin
@admin.register(PrescriptionTest)
class PrescriptionTestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'prescription',
        'lab_test',
        'priority',
        'status',
        'lab_user',
        'created_at'
    ]

    list_filter = ['status', 'priority', 'lab_test']
    search_fields = ['prescription__id', 'lab_test__name']

    readonly_fields = ['created_at']

    list_editable = ['status', 'priority']