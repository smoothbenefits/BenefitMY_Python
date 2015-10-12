from django.http import HttpResponse

from rest_framework.views import APIView

from app.views.permission import (
    user_passes_test,
    company_employer_or_broker)
from app.service.Report.company_employee_benefit_pdf_report_service import \
    CompanyEmployeeBenefitPdfReportService


class CompanyUsersSummaryPdfExportView(APIView):

    @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="employee_benefit_summary.pdf"'

        # Generate the report
        pdf_service = CompanyEmployeeBenefitPdfReportService()
        pdf_service.get_all_employees_resport(pk, response)

        return response
