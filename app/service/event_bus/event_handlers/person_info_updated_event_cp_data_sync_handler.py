from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.person_info_updated_event import PersonInfoUpdatedEvent
from app.models.person import (Person, SELF)
from app.service.integration.payroll.connect_payroll.connect_payroll_data_service import ConnectPayrollDataService
from app.service.company_personnel_service import CompanyPersonnelService


class PersonInfoUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(PersonInfoUpdatedEventCpDataSyncHandler, self).__init__(PersonInfoUpdatedEvent)
        self._cp_data_service = ConnectPayrollDataService()
        self._company_personnel_service = CompanyPersonnelService()

    def _internal_handle(self, event):
        person_model = Person.objects.get(pk=event.person_id)

        # We only attempt at syncing data if the person updated is 
        # the employee, and not family members
        if (not person_model.relationship == SELF):
            return 

        # We only proceed if we are looking at an employee, and not other roles
        if (not self._company_personnel_service.is_user_employee(person_model.user.id)):
            return

        # No-op if the employee (the company he/she belongs to) is not using 
        # the integration service in context
        if (not self._cp_data_service.is_supported(person_model.user.id)):
            return

        self._cp_data_service.sync_employee_data_to_remote(person_model.user.id)
