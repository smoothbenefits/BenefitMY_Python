from datetime import date
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.views.reports.report_export_view_base import ReportExportViewBase
from app.service.Report.integration.advantage_payroll.advantage_payroll_period_export_csv_service \
    import AdvantagePayrollPeriodExportCsvService
from app.service.date_time_service import DateTimeService


class AdvantagePayrollPeriodExportCsvView(ReportExportViewBase):

    def get(self, request, company_id, format=None):
        csv_service = AdvantagePayrollPeriodExportCsvService()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=period_data_export.csv'
        
        # For now assume the report time period is the current week
        date_time_service = DateTimeService()
        today = date.today()
        time_range = date_time_service.get_week_range_by_date(today)

        csv_service.get_report(company_id, time_range[0], time_range[1], response)

        return response
