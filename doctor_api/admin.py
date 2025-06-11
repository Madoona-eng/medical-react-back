from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience')
    search_fields = ('user__username', 'user__email', 'specialty')
    list_filter = ('specialty',)