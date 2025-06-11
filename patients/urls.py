from django.urls import path
from .views import (
    DoctorListView,
    SpecialtyListView,
    AppointmentCreateView,
    PatientAppointmentListView,
    PatientProfileView
)

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('specialties/', SpecialtyListView.as_view(), name='specialty-list'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('my-appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),  
]