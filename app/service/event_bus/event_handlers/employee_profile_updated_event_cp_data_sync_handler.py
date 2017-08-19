from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.employee_profile_updated_event import EmployeeProfileUpdatedEvent
from app.models.person import (Person, SELF)
from app.service.integration.company_integration_provider_data_service import CompanyIntegrationProviderDataService


class EmployeeProfileUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(EmployeeProfileUpdatedEventCpDataSyncHandler, self).__init__(EmployeeProfileUpdatedEvent)
        self._cp_data_service = CompanyIntegrationProviderDataService()

    def _internal_handle(self, event):
        self._cp_data_service.sync_employee_data_to_remote(event.user_id)
