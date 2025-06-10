from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)  # only for doctors

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    
    
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    patientName = models.CharField(max_length=100)
    doctor = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'Doctor'})
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.patientName} - {self.doctor.username} ({self.date} {self.time})"
    
