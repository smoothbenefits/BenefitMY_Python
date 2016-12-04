from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.views.reports.report_export_view_base import ReportExportViewBase
from app.service.Report.integration.advantage_payroll.advantage_payroll_company_setup_csv_service \
    import AdvantagePayrollCompanySetupCsvService


class AdvantagePayrollClientSetupCsvView(ReportExportViewBase):

    def get(self, request, company_id, format=None):
        csv_service = AdvantagePayrollCompanySetupCsvService()

        response = HttpResponse(content_type='text/cvs')
        response['Content-Disposition'] = 'attachment; filename=client_setup.csv'
        
        csv_service.get_report(company_id, response)

        return response
