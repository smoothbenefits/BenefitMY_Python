from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from .event_handler_base import EventHandlerBase
from ..events.time_12am_est_event import Time12AMESTEvent
from ..events.company_daily_time_card_audit_requested_event import CompanyDailyTimeCardAuditEvent
from ..aws_event_bus_service import AwsEventBusService
from app.service.application_feature_service import (
    ApplicationFeatureService,
    APP_FEATURE_RANGEDTIMECARD,
    APP_FEATURE_TIMEPUNCHCARDAUDITREPORT
)


class DailyTimeCardAuditReportHandler(EventHandlerBase):
    _aws_event_bus_service = AwsEventBusService()
    _application_feature_service = ApplicationFeatureService()

    def __init__(self):
        super(DailyTimeCardAuditReportHandler, self).__init__(Time12AMESTEvent)
    
    def _internal_handle(self, event):
        # Fan out (sub) events for each company that currently has the time card
        # feature on and has the audit enabled
        with_time_card_feature_on = self._application_feature_service.get_company_list_with_feature_enabled(APP_FEATURE_RANGEDTIMECARD)
        with_report_feature_on = self._application_feature_service.get_company_list_with_feature_enabled(APP_FEATURE_TIMEPUNCHCARDAUDITREPORT)

        company_list = list(set(with_time_card_feature_on) & set(with_report_feature_on))

        for company in company_list:
            event = CompanyDailyTimeCardAuditEvent(company)
            self._aws_event_bus_service.publish_event(event)
