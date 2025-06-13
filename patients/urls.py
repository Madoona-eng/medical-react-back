from django.urls import path
from .views import (
    DoctorListView,
    SpecialtyListView,
    AppointmentCreateView,
    PatientAppointmentListView,
    PatientProfileView
)
from .views import AppointmentUpdateView, cancel_appointment

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('specialties/', SpecialtyListView.as_view(), name='specialty-list'),
    path('appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('my-appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('profile/', PatientProfileView.as_view(), name='patient-profile'),  
    path('appointments/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/cancel/', cancel_appointment, name='appointment-cancel'),
]