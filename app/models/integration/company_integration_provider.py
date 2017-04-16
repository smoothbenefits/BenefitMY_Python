import reversion
from django.db import models
from app.models.company import Company
from app.models.integration.integration_provider import IntegrationProvider


@reversion.register
class CompanyIntegrationProvider(models.Model):
    company = models.ForeignKey(Company, related_name="integration_provider")
    integration_provider = models.ForeignKey(IntegrationProvider, related_name="company_list")
    
    # As a common requirement for most of the integrations, our system would need
    # to acquire and store the ID from the external system to properly identify
    # the company in our system, and use that ID to communicate with external system.
    # E.g. as part of the initial handshake with a payroll system, we need to get the 
    # ID from the payroll system that identify this company as their client on that 
    # system.
    company_external_id = models.CharField(max_length=255, null=True, blank=True)

    # Optional
    # In the case where the external id for employees need to be 
    # generated on the WBM system, we need to know where to start
    # There would be default logic built, such as starting at the 
    # max employee ID currently exists. But there are often cases
    # where this starting point needs to be forcely set. And this
    # below field is for this purpose
    employee_external_id_seed = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('company', 'integration_provider'), ('company_external_id', 'integration_provider'))
