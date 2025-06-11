from django.db import models
from accounts.models import CustomUser  # Import from accounts

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    patientName = models.CharField(max_length=100, default="Unknown", null=True, blank=True)
    doctor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'Doctor'}, related_name='patients_doctor_appointments', null=True, blank=True)
    date = models.DateField(default=None, null=True, blank=True)
    time = models.TimeField(default=None, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.patientName} - {self.doctor.username if self.doctor else 'No Doctor'} ({self.date} {self.time})"