from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.views.reports.report_export_view_base import ReportExportViewBase
from app.service.Report.integration.advantage_payroll.advantage_payroll_period_export_csv_service \
    import AdvantagePayrollPeriodExportCsvService


class AdvantagePayrollPeriodExportCsvView(ReportExportViewBase):

    def get(self, request, company_id, format=None):
        csv_service = AdvantagePayrollPeriodExportCsvService()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=period_data_export.csv'
        
        csv_service.get_report(company_id, response)

        return response
