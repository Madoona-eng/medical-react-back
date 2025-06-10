from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience')
    search_fields = ('user__username', 'user__email', 'specialty')
    list_filter = ('specialty',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('doctor__user__username', 'patient__username', 'reason')