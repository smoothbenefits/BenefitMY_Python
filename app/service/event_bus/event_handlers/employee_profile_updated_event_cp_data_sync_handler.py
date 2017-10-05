from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.employee_profile_updated_event import EmployeeProfileUpdatedEvent
from app.service.integration.payroll.connect_payroll.connect_payroll_data_service import ConnectPayrollDataService
from app.service.company_personnel_service import CompanyPersonnelService


class EmployeeProfileUpdatedEventCpDataSyncHandler(EventHandlerBase):
    def __init__(self):
        super(EmployeeProfileUpdatedEventCpDataSyncHandler, self).__init__(EmployeeProfileUpdatedEvent)
        self._cp_data_service = ConnectPayrollDataService()
        self._company_personnel_service = CompanyPersonnelService()

    def _internal_handle(self, event):
        # We only proceed if we are looking at an employee, and not other roles
        if (not self._company_personnel_service.is_user_employee(event.user_id)):
            return
        
        # No-op if the employee (the company he/she belongs to) is not using 
        # the integration service in context
        if (not self._cp_data_service.is_supported(event.user_id)):
            return

        self._cp_data_service.sync_employee_data_to_remote(event.user_id)
