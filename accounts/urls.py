from django.urls import path

from .views import (
    RegisterView, LoginView,
    UsersListView, UserDeleteView,
    DoctorListCreateView, DoctorDetailView,
    SpecialtiesView,
    SpecialtyListCreateView,
    SpecialtyDetailView,
    AppointmentListView,
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UsersListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    
    path('doctors', DoctorListCreateView.as_view()),
    path('doctors/<int:pk>', DoctorDetailView.as_view()),
    path('specialtiesData', SpecialtiesView.as_view()),
    
    path('specialtiesData/', SpecialtyListCreateView.as_view()),
    path('specialtiesData/<int:pk>/', SpecialtyDetailView.as_view()),
    
    path('appointments', AppointmentListView.as_view()),
]
