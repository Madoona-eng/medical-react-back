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
    patientName = serializers.CharField(read_only=True)
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
    name = serializers.CharField(source='username', required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'first_name', 'last_name', 'image']
        extra_kwargs = {
            'email': {'required': False},
            'name': {'required': False},
            'phone': {'required': False},
        }

    def update(self, instance, validated_data):
        # Handle image upload separately if needed
        image = validated_data.pop('image', None)
        if image:
            instance.image = image
        # Handle username (name)
        if 'username' in validated_data:
            instance.username = validated_data['username']
        # Handle phone
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        # Handle email
        if 'email' in validated_data:
            instance.email = validated_data['email']
        # Handle first_name and last_name
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        instance.save()
        return instance