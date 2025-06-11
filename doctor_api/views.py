from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer
from django.utils import timezone

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def specialties(self, request):
        return Response([
            "Cardiology", "Neurology", "Dermatology",
            "Pediatrics", "Orthopedics"
        ])

    @action(detail=True, methods=['POST'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        doctor = self.get_object()
        doctor.image = request.FILES['image']
        doctor.save()
        return Response({'image_url': doctor.image.url})

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Appointment.objects.filter(doctor=self.request.user.doctor)
        if self.request.query_params.get('upcoming'):
            return queryset.filter(date__gte=timezone.now().date())
        elif self.request.query_params.get('past'):
            return queryset.filter(date__lt=timezone.now().date())
        return queryset

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    doctor = request.user.doctor
    return Response({
        'total_patients': Appointment.objects.filter(doctor=doctor).count(),
        'today_appointments': Appointment.objects.filter(
            doctor=doctor,
            date=timezone.now().date()
        ).count(),
        'weekly_appointments': [12, 19, 8, 15, 10],  # Mock data
        'patient_types': [  # Mock data
            {'type': 'New', 'count': 30},
            {'type': 'Follow-up', 'count': 50},
            {'type': 'Emergency', 'count': 20}
        ]
    })