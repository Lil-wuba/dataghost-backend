"""dataghost URL Configuration

This file routes URLs to views or other URL configs.
For beginners: Think of this as the main router for your app.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # For login: POST username/password to get tokens
    TokenRefreshView,     # For refreshing access token
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Default admin panel
    path('api/', include('core.urls')),  # Include our app's URLs under /api/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login API
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]