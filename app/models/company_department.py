from django.db import models
from company import Company

class CompanyDepartment(models.Model):
    company = models.ForeignKey(Company, related_name='company_company_department')
    department = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
    	unique_together = ('company', 'department')
