from django.shortcuts import render
from accounts.models import CustomUser  # Instead of from .models
from .models import Appointment, Specialty
# Create your views here.
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import CustomUser, Appointment, Specialty
from .serializers import DoctorSerializer, SpecialtySerializer, AppointmentSerializer,PatientProfileSerializer

class DoctorListView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return CustomUser.objects.filter(role='Doctor')

class SpecialtyListView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Automatically set the patient name from the logged-in user
        serializer.save(patientName=self.request.user.username)

class PatientAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Appointment.objects.filter(patientName=self.request.user.username)
class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return Response(serializer.data)