import reversion
from django.db import models
from app.models.company import Company

@reversion.register
class CompanyServiceProvider(models.Model):
    company = models.ForeignKey(Company, related_name="service_provider")
    provider_type = models.CharField(max_length=255)
    name = models.CharField(max_length=1024)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    link = models.CharField(max_length=1024, null=True, blank=True)
    show_to_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
