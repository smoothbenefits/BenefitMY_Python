import reversion
from django.db import models
from app.models.company_user import CompanyUser
from app.models.integration.integration_provider import IntegrationProvider


@reversion.register
class CompanyUserIntegrationProvider(models.Model):
    company_user = models.ForeignKey(CompanyUser, related_name="integration_provider")
    integration_provider = models.ForeignKey(IntegrationProvider, related_name="company_user_list")
    
    # As a common requirement for most of the integrations, our system would need
    # to acquire and store the ID from the external system to properly identify
    # the company_user (i.e. employee) in our system, and use that ID to communicate with external system.
    # E.g. as part of the initial employee payroll setup with a payroll system, we need to get the 
    # ID from the payroll system that identify this company_user with their record id on that 
    # system.
    company_user_external_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('company_user', 'integration_provider'), ('company_user_external_id', 'integration_provider'))
