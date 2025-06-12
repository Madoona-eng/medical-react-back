from django.contrib import admin

from .models import Specialty

from .models import CustomUser, Appointment  # Add your models here

admin.site.register(Specialty)

admin.site.register(CustomUser)

#admin.site.register(Appointment)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "patientName", "date", "time", "status")