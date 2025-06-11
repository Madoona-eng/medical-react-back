from django.apps import AppConfig


class DoctorApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor_api'

    def ready(self):
        import doctor_api.signals  # Connect the signals
