from rest_framework import serializers
from .models import Doctor, Appointment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'name', 'specialty', 'bio', 'image_url', 'phone', 'availability']

    def get_name(self, obj):
        return f"Dr. {obj.user.last_name}"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def validate_availability(self, value):
        import re
        for day, slots in value.items():
            for slot in slots:
                if not re.match(r'^\d{2}:\d{2}-\d{2}:\d{2}$', slot):
                    raise serializers.ValidationError("Time slots must be in HH:MM-HH:MM format")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['doctor']