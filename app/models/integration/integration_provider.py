import reversion

from django.db import models

INTEGRATION_SERVICE_TYPE_PAYROLL = 'Payroll'
INTEGRATION_SERVICE_TYPES = ([(item, item) for item in [INTEGRATION_SERVICE_TYPE_PAYROLL]])


@reversion.register
class IntegrationProvider(models.Model):
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=30, choices=INTEGRATION_SERVICE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '[' + self.service_type + '] ' + self.name

    class Meta:
        unique_together = ('name', 'service_type')
