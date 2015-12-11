from django.db import models
from company import Company

class CompanyGroup(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
