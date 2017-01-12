from datetime import date
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.views.reports.report_export_view_base import ReportExportViewBase
from app.service.Report.integration.advantage_payroll.advantage_payroll_period_export_csv_service \
    import AdvantagePayrollPeriodExportCsvService
from app.service.date_time_service import DateTimeService


class AdvantagePayrollPeriodExportCsvView(ReportExportViewBase):

    def get(self, request, company_id,
        from_year, from_month, from_day,
        to_year, to_month, to_day, format=None):
        period_start = date(year=int(from_year), month=int(from_month), day=int(from_day))
        period_end = date(year=int(to_year), month=int(to_month), day=int(to_day))

        csv_service = AdvantagePayrollPeriodExportCsvService()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=period_data_export.csv'

        csv_service.get_report(company_id, period_start, period_end, response)

        return response
