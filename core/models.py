from django.db import models

# Models define the database structure.
# Each class here becomes a table in SQLite.

class Asset(models.Model):
    # Choices for asset_type field - limits options to these.
    ASSET_TYPES = (
        ('Server', 'Server'),
        ('Endpoint', 'Endpoint'),
        ('Cloud', 'Cloud'),
    )
    
    name = models.CharField(max_length=255)  # Short text field for name
    ip_address = models.CharField(max_length=255)  # Short text for IP (could be IPv4/IPv6)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)  # Dropdown-like choices
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set to now when created
    
    def __str__(self):
        return self.name  # What shows in admin or queries

class Vulnerability(models.Model):
    # Choices for severity and status.
    SEVERITIES = (
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )
    STATUSES = (
        ('Open', 'Open'),
        ('Fixed', 'Fixed'),
    )
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Link to Asset; delete vulns if asset deleted
    name = models.CharField(max_length=255)  # Vulnerability name (e.g., CVE-XXXX)
    description = models.TextField()  # Longer text for details
    severity = models.CharField(max_length=50, choices=SEVERITIES)  # Severity level
    status = models.CharField(max_length=50, choices=STATUSES, default='Open')  # Default to Open
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set creation time
    
    def __str__(self):
        return f"{self.name} ({self.severity})"