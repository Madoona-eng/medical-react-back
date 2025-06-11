from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token authentication
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('', include('rest_framework.urls')),  # Browsable API login
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
