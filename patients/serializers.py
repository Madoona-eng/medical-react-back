from rest_framework import serializers
from accounts.models import CustomUser  # Use correct import
from .models import Appointment, Specialty

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'image', 'specialty']
        
class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='Doctor'),
        source='doctor',
        write_only=True
    )
    
    class Meta:
        model = Appointment
        fields = ['id', 'patientName', 'doctor', 'doctor_id', 'date', 'time', 'status']
        extra_kwargs = {
            'status': {'read_only': True}
        }

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # Handle image upload separately if needed
        image = validated_data.pop('image', None)
        if image:
            instance.image = image
        return super().update(instance, validated_data)