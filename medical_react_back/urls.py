from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include([
        path('doctors/', include('doctor_api.urls')),  # Doctor API endpoints
        path('patients/', include('patients.urls')),    # Patient API endpoints
        path('accounts/', include('accounts.urls')),    # Account management
    ])),
    
    # Authentication Endpoints
    path('api/auth/', include([
        path('token/', obtain_auth_token, name='api_token_auth'),  # Token authentication
        path('', include('rest_framework.urls')),  # Browsable API login
    ])),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)