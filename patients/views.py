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
        # Always set patientName from the logged-in user's username (from token)
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
        validated_data = serializer.validated_data
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'image' in validated_data:
            instance.image = validated_data['image']
        instance.save()
        # Return only name, email, and phone in the response
        response_data = {
            'name': instance.username,
            'email': instance.email,
            'phone': getattr(instance, 'phone', None)
        }
        return Response(response_data)