from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.views.reports.report_export_view_base import ReportExportViewBase
from app.service.Report.integration.connect_payroll.connect_payroll_company_employee_front_page_csv_service \
    import ConnectPayrollCompanyEmployeeFrontPageCsvService


class ConnectPayrollEmployeeFrontPageCsvView(ReportExportViewBase):

    def get(self, request, company_id, format=None):
        csv_service = ConnectPayrollCompanyEmployeeFrontPageCsvService()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=employee_frontpage.csv'
        
        csv_service.get_report(company_id, response)

        return response
