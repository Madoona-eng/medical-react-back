from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from accounts.models import Appointment, CustomUser
from .serializers import DoctorSerializer, AppointmentSerializer, UserSerializer
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import parser_classes
import re

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def my_profile(self, request):
        """Get complete profile information for the logged-in doctor"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            serializer = self.get_serializer(doctor)
            appointments = Appointment.objects.filter(doctor=request.user)
            today_appointments = appointments.filter(date=timezone.now().date()).count()
            
            response_data = serializer.data
            response_data.update({
                'user': {
                    'email': request.user.email,
                    'full_name': request.user.get_full_name(),
                    'username': request.user.username,
                    'image': request.user.image.url if request.user.image else None,
                },
                'stats': {
                    'total_appointments': appointments.count(),
                    'today_appointments': today_appointments,
                    'pending_appointments': appointments.filter(status='pending').count(),                }
            })
            return Response(response_data)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=False, methods=['PUT', 'PATCH'])
    def update_profile(self, request):
        """Update doctor's profile information"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            user = request.user

            # Update User model fields
            user_data = request.data.get('user', {})
            if user_data:
                if 'first_name' in user_data:
                    user.first_name = user_data['first_name']
                if 'last_name' in user_data:
                    user.last_name = user_data['last_name']
                if 'email' in user_data:
                    if CustomUser.objects.exclude(id=user.id).filter(email=user_data['email']).exists():
                        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
                    user.email = user_data['email']
                user.save()            # Update Doctor model fields
            doctor_data = request.data.get('profile', {})
            if doctor_data:
                if 'specialty' in doctor_data:
                    doctor.specialty = doctor_data['specialty']
                if 'experience' in doctor_data:
                    doctor.experience = doctor_data['experience']
                if 'bio' in doctor_data:
                    doctor.bio = doctor_data['bio']
                if 'availability' in doctor_data:
                    # Validate availability through serializer
                    serializer = self.get_serializer(instance=doctor)
                    try:
                        availability = serializer.validate_availability(doctor_data['availability'])
                        doctor.availability = availability
                    except serializers.ValidationError as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                doctor.save()
            return self.my_profile(request)

        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['POST'])
    def update_image(self, request):
        """Update doctor's profile image"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            
            if 'profile_image' not in request.FILES:
                return Response(
                    {"error": "Profile image is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update both profile_image in Doctor model and image in CustomUser model
            image_file = request.FILES['profile_image']
            doctor.profile_image = image_file
            doctor.user.image = image_file  # Update user's image as well
            doctor.save()
            doctor.user.save()
            doctor.user.save()

            return Response({
                'status': 'success',
                'data': {
                    'doctor_profile_image': doctor.profile_image.url if doctor.profile_image else None,
                    'user_image': doctor.user.image.url if doctor.user.image else None,
                    'file_name': image_file.name,
                    'file_size': f"{image_file.size / 1024:.2f} KB",
                    'file_type': image_file.content_type
                }
            })

        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['POST'])
    def change_password(self, request):
        """Change doctor's password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {"error": "Current password is incorrect"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"})

    @action(detail=False, methods=['GET'])
    def specialties(self, request):
        specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
        return Response(list(specialties))

    @action(detail=True, methods=['POST'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        doctor = self.get_object()
        doctor.image = request.FILES['image']
        doctor.save()
        return Response({'image_url': doctor.image.url})

    @action(detail=False, methods=['GET'])
    def availability(self, request):
        """Get doctor's availability schedule"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            return Response(doctor.get_availability())
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['POST'])
    def set_availability(self, request):
        """Set doctor's availability for specific days"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            data = request.data

            # Validate the time slots format
            DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            TIME_SLOT_PATTERN = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
            
            for day, slots in data.items():
                # Validate day
                if day.lower() not in DAYS:
                    return Response(
                        {"error": f"Invalid day: {day}. Must be one of {DAYS}"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Validate time slots
                if not isinstance(slots, list):
                    return Response(
                        {"error": f"Time slots for {day} must be a list"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                for slot in slots:
                    if not re.match(TIME_SLOT_PATTERN, slot):
                        return Response(
                            {"error": f"Invalid time slot format: {slot}. Must be HH:MM-HH:MM"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Validate time logic
                    start, end = slot.split('-')
                    if start >= end:
                        return Response(
                            {"error": f"Invalid time slot: {slot}. Start time must be before end time"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )

                doctor.set_availability(day.lower(), slots)

            return Response({
                "message": "Availability updated successfully",
                "availability": doctor.get_availability()
            })

        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'])
    def day_availability(self, request):
        """Get doctor's availability for a specific day"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            day = request.query_params.get('day', '').lower()
            
            if not day:
                return Response(
                    {"error": "Day parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                day: doctor.get_availability(day)
            })

        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['DELETE'])
    def delete_availability(self, request):
        """Delete availability for specific days or all days"""
        try:
            doctor = Doctor.objects.get(user=request.user)
            days = request.query_params.getlist('days', [])
            
            if not days:
                # Delete all availability
                doctor.availability = {}
                doctor.save()
                return Response({
                    "message": "All availability deleted successfully",
                    "availability": {}
                })
            
            # Delete specific days
            current_availability = doctor.availability or {}
            for day in days:
                day = day.lower()
                if day in current_availability:
                    del current_availability[day]
            
            doctor.availability = current_availability
            doctor.save()
            
            return Response({
                "message": f"Availability deleted for days: {', '.join(days)}",
                "availability": doctor.availability
            })

        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_appointments(self, request):
        """Get all appointments for the logged-in doctor"""
        if request.user.role != 'Doctor':
            return Response({"error": "Only doctors can access appointments"}, status=status.HTTP_403_FORBIDDEN)
            
        appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def update_appointment_status(self, request, pk=None):
        """Update the status of a specific appointment"""
        try:
            appointment = Appointment.objects.get(pk=pk, doctor=request.user)
            new_status = request.data.get('status')
            
            if not new_status or new_status not in dict(Appointment.STATUS_CHOICES):
                return Response(
                    {"error": "Invalid status. Must be one of: pending, confirmed, cancelled"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            appointment.status = new_status
            appointment.save()
            
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)
            
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found or you don't have permission to modify it"},
                status=status.HTTP_404_NOT_FOUND
            )

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user).order_by('date', 'time')

    def create(self, request, *args, **kwargs):
        # Ensure the doctor field is set to the logged-in user
        request.data['doctor'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Only allow updating the status
        if 'status' in request.data:
            if request.data['status'] not in dict(Appointment.STATUS_CHOICES):
                return Response(
                    {"error": "Invalid status. Must be one of: pending, confirmed, cancelled"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance.status = request.data['status']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(
            {"error": "Only status field can be updated"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    if request.user.role != 'Doctor':
        return Response({"error": "Only doctors can access dashboard stats"}, status=status.HTTP_403_FORBIDDEN)
    
    today = timezone.now().date()
    appointments = Appointment.objects.filter(doctor=request.user)
    
    return Response({
        'total_appointments': appointments.count(),
        'today_appointments': appointments.filter(date=today).count(),
        'pending_appointments': appointments.filter(status='pending').count(),
    })