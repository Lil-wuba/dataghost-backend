from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Asset, Vulnerability
from .serializers import AssetSerializer, VulnerabilitySerializer

# Views handle API logic.
# generics provide ready-made classes for list/create/update.

class AssetListCreateView(generics.ListCreateAPIView):
    # GET: List all assets; POST: Create new asset.
    queryset = Asset.objects.all()  # All assets
    serializer_class = AssetSerializer  # Use this serializer
    permission_classes = [IsAuthenticated]  # Require JWT auth

class VulnerabilityListCreateView(generics.ListCreateAPIView):
    # GET: List vulnerabilities; POST: Create new.
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]

class VulnerabilityUpdateView(generics.UpdateAPIView):
    # PATCH: Update a vulnerability (restricted to status only).
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        # Check if only 'status' is being updated (as per requirements).
        if set(request.data.keys()) - {'status'}:
            return Response({'error': 'Only status can be updated'}, status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)  # Proceed with update if valid

class DashboardView(APIView):
    # GET: Return dashboard stats in JSON.
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Count total vulnerabilities.
        total_vulns = Vulnerability.objects.count()
        
        # Group by severity and count.
        severity_breakdown = Vulnerability.objects.values('severity').annotate(count=Count('severity'))
        breakdown = {item['severity']: item['count'] for item in severity_breakdown}
        
        # Total assets.
        total_assets = Asset.objects.count()
        
        # Build the response JSON.
        data = {
            'total_vulnerabilities': total_vulns,
            'critical': breakdown.get('Critical', 0),
            'high': breakdown.get('High', 0),
            'medium': breakdown.get('Medium', 0),
            'low': breakdown.get('Low', 0),
            'total_assets': total_assets
        }
        return Response(data)

class RegisterView(APIView):
    # POST: Register a new user (no auth required).
    permission_classes = [AllowAny]  # Open to anyone
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Basic validation.
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user (password is hashed automatically).
        User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)