from django.db import models
from accounts.models import CustomUser, Appointment

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    experience = models.IntegerField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(blank=True)
    availability = models.JSONField(default=dict)  # Store availability as JSON
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"
    
    def set_availability(self, day, time_slots):
        if not self.availability:
            self.availability = {}
        self.availability[day] = time_slots
        self.save()
    
    def get_availability(self, day=None):
        if not self.availability:
            return {}
        if day:
            return self.availability.get(day, [])
        return self.availability
