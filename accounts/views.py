from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserListSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DoctorSerializer
from django.db.models import Q
from .models import Specialty
from .serializers import SpecialtySerializer
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.generics import ListAPIView

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = RegisterSerializer(user).data  # Reuse existing serializer
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UsersListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = []  # Optional: use [IsAuthenticated] if needed

class UserDeleteView(APIView):
    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class DoctorListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='Doctor')
    serializer_class = DoctorSerializer

class DoctorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.filter(role='Doctor')
    serializer_class = DoctorSerializer
    lookup_field = 'pk'

class SpecialtiesView(APIView):
    def get(self, request):
        specialties = [
            "Cardiology", "Dermatology", "Neurology", "Pediatrics", "Psychiatry",
            "Oncology", "Orthopedics", "Radiology", "Urology"
        ]
        return Response({"specialties": specialties})
    
    
    

class SpecialtyListCreateView(APIView):
    def get(self, request):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecialtySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialtyDetailView(APIView):
    def put(self, request, pk):
        try:
            specialty = Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response({"error": "Specialty not found"}, status=404)

        serializer = SpecialtySerializer(specialty, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            specialty = Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response({"error": "Specialty not found"}, status=404)
        
        specialty.delete()
        return Response(status=204)
    
class AppointmentListView(ListAPIView):
    queryset = Appointment.objects.all().order_by('-date', '-time')  # Optional: sort by latest
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]  # ✅ Require login to access
