from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.employee_profile_updated_event import EmployeeProfileUpdatedEvent
from app.service.integration.payroll.connect_payroll.connect_payroll_data_service import ConnectPayrollDataService


class EmployeeProfileUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(EmployeeProfileUpdatedEventCpDataSyncHandler, self).__init__(EmployeeProfileUpdatedEvent)
        self._cp_data_service = ConnectPayrollDataService()

    def _internal_handle(self, event):
        # No-op if the employee (the company he/she belongs to) is not using 
        # the integration service in context
        if (not self._cp_data_service.is_supported(event.user_id)):
            return

        self._cp_data_service.sync_employee_data_to_remote(event.user_id)
