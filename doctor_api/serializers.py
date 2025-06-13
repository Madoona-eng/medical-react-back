from rest_framework import serializers
from .models import Doctor
from accounts.models import CustomUser, Appointment
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','id']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    availability = serializers.JSONField(required=False)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'name', 'specialty', 'experience', 'bio', 'image_url', 'availability']

    def get_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"

    def get_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

    def validate_availability(self, value):
        if value:
            DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            TIME_SLOT_PATTERN = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
            
            for day, slots in value.items():
                if day.lower() not in DAYS:
                    raise serializers.ValidationError(f"Invalid day: {day}")
                
                if not isinstance(slots, list):
                    raise serializers.ValidationError(f"Time slots for {day} must be a list")
                
                for slot in slots:
                    if not re.match(TIME_SLOT_PATTERN, slot):
                        raise serializers.ValidationError(
                            f"Invalid time slot format: {slot}. Must be HH:MM-HH:MM"
                        )
                    
                    start, end = slot.split('-')
                    if start >= end:
                        raise serializers.ValidationError(
                            f"Invalid time slot: {slot}. Start time must be before end time"
                        )
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patientName', 'date', 'time', 'status', 'doctor']
        read_only_fields = ['doctor']