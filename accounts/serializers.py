from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from .models import Specialty
from .models import Appointment

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'role', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    name = serializers.CharField(source='username')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    

class UserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'role', 'image']


class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'image', 'role', 'specialty']

    def create(self, validated_data):
        validated_data['username'] = validated_data.get('username') or validated_data.get('name')
        validated_data['password'] = make_password('12345678')  # default password if needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.specialty = validated_data.get('specialty', instance.specialty)

        image = validated_data.get('image')
        if image:
            instance.image = image
        instance.save()
        return instance


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']
        

class AppointmentSerializer(serializers.ModelSerializer):
    doctorId = serializers.IntegerField(source='doctor.id')
    
    class Meta:
        model = Appointment
        fields = ['id', 'patientName', 'doctorId', 'date', 'time', 'status']