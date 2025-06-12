from django.db import models
from accounts.models import CustomUser, Appointment  # Import Appointment once
from accounts.models import Appointment  # ✅ Only use this import

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name  # ✅ use __str__ not str for correct model display
