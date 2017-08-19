from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.person_info_updated_event import PersonInfoUpdatedEvent
from app.models.person import (Person, SELF)
from app.service.integration.company_integration_provider_data_service import CompanyIntegrationProviderDataService


class PersonInfoUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(PersonInfoUpdatedEventCpDataSyncHandler, self).__init__(PersonInfoUpdatedEvent)
        self._cp_data_service = CompanyIntegrationProviderDataService()

    def _internal_handle(self, event):
        person_model = Person.objects.get(pk=event.person_id)

        # We only attempt at syncing data if the person updated is 
        # the employee, and not family members
        if (not person_model.relationship == SELF):
            return 

        self._cp_data_service.sync_employee_data_to_remote(person_model.user.id)
