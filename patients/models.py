from django.db import models
from accounts.models import CustomUser, Appointment  # Import from accounts
# Remove Appointment model definition from patients/models.py if it exists

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def str(self):
        return self.name