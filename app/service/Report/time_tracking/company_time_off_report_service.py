from datetime import date
from dateutil import rrule
import json

from django.contrib.auth import get_user_model

from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.time_off_service import (
    TimeOffService,
    TIME_OFF_STATUS_APPROVED,
    TIME_OFF_STATUS_PENDING
)
from app.service.Report.csv_report_service_base import CsvReportServiceBase

User = get_user_model()


class CompanyTimeOffReportService(CsvReportServiceBase):

    def __init__(self):
        super(CompanyTimeOffReportService, self).__init__()
        self.view_model_factory = ReportViewModelFactory()
        self.time_off_service = TimeOffService()

    def get_report(self, company_id, period_start, period_end, outputStream):
        self._write_headers()
        self._write_company(company_id, period_start, period_end)
        self._save(outputStream)

    def _write_headers(self):
        self._write_cell('Employee Name')
        self._write_cell('Total Approved Hours')
        self._write_cell('Total Pending Hours')
        self._next_row()
        self._write_cell('')
        self._write_cell('Record Type')
        self._write_cell('Start Time')
        self._write_cell('Duration')
        self._write_cell('Status')
        self._write_cell('Decision Time')
        self._write_cell('Approver Name')

    def _write_company(self, company_id, period_start, period_end):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # Get the time tracking data for the company, for the date period
        # specified
        # all_records = self.time_off_service.get_company_users_time_off_records_by_date_range(
        #     company_id, period_start, period_end)

        # print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        # for record in all_records:
        #     print '{0} {1} {2} {3}'.format(record.requestor_full_name, self._get_date_string(record.start_date_time), record.record_type, self._normalize_decimal_number(record.duration))

        # Get the time tracking data for the company, for the date period
        # specified
        all_aggregates = self.time_off_service.get_company_users_time_off_record_aggregates_by_date_range(
            company_id, period_start, period_end)

        print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        for aggregate in all_aggregates:
            print '{0} {1} {2}'.format(
                aggregate.employee_full_name,
                self._normalize_decimal_number(aggregate.get_total_hours_by_record_status(TIME_OFF_STATUS_APPROVED)),
                self._normalize_decimal_number(aggregate.get_total_hours_by_record_status(TIME_OFF_STATUS_PENDING))
            )

    def _write_employee(self):
        pass

    def _normalize_decimal_number(self, decimal_number):
        result = decimal_number
        if (decimal_number == 0 or decimal_number):
            result = "{:.2f}".format(float(decimal_number))
        return result
