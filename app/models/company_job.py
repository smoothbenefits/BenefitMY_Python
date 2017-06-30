from django.db import models
from company import Company


class CompanyJob(models.Model):
    company = models.ForeignKey(Company, related_name='company_company_job')
    job = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    code = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('company', 'job')
