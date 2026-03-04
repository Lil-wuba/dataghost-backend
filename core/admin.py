from django.contrib import admin
from .models import Asset, Vulnerability

admin.site.register(Asset)
admin.site.register(Vulnerability)