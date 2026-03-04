from django.urls import path
from .views import (
    AssetListCreateView,
    VulnerabilityListCreateView,
    VulnerabilityUpdateView,
    DashboardView,
    RegisterView,
)

urlpatterns = [
    # Assets
    path('assets/', AssetListCreateView.as_view()),
    
    # Vulnerabilities
    path('vulnerabilities/', VulnerabilityListCreateView.as_view()),
    path('vulnerabilities/<int:pk>/', VulnerabilityUpdateView.as_view()),
    
    # Dashboard
    path('dashboard/', DashboardView.as_view()),
    
    # Register
    path('register/', RegisterView.as_view()),
]