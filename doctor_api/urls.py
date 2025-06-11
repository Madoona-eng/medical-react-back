from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.DoctorViewSet, basename='doctor')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
]