from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.time_11pm_utc_event import Time11PMUTCEvent
from ..events.company_daily_employee_data_change_report_event import CompanyDailyEmployeeDataChangeReportEvent
from ..aws_event_bus_service import AwsEventBusService
from app.service.application_feature_service import (
    ApplicationFeatureService,
    APP_FEATURE_EMPLOYEEDATACHANGENOTIFICATION
)


class DailyEmployeeDataChangeReportHandler(EventHandlerBase):
    _aws_event_bus_service = AwsEventBusService()
    _application_feature_service = ApplicationFeatureService()

    def __init__(self):
        super(DailyEmployeeDataChangeReportHandler, self).__init__(Time11PMUTCEvent)
    
    def _internal_handle(self, event):
        # Fan out (sub) events for each company that currently the feature is enabled 
        company_list = self._application_feature_service.get_company_list_with_feature_enabled(APP_FEATURE_EMPLOYEEDATACHANGENOTIFICATION)

        for company in company_list:
            event = CompanyDailyEmployeeDataChangeReportEvent(company)
            self._aws_event_bus_service.publish_event(event)
