from datetime import date
from django.http import HttpResponse
from django.http import Http404

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ...report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory

from app.service.contractor_service import ContratorService
from app.models.company import Company

class FormLienWaiverView(ReportExportViewBase):

    def get(self, request, company_id, contractor_id, format=None):

        # Get date tokens
        today_date = date.today()
        month_name = today_date.strftime('%B')
        day = today_date.day
        year_last2 = today_date.strftime('%y')

        # Get Contractor Info
        contractor_service = ContratorService()
        contractor_info = contractor_service.get_contractor_by_id(contractor_id)
        if (not contractor_info):
            # Not able to locate resource per the given 
            # contractor ID
            raise 404
        contractor_name = contractor_info['name']

        # Get Company Info
        company = Company.objects.get(pk=company_id)
        company_name = company.name

        # Populate the form fields
        fields = {
            'body_month': month_name,
            'body_day': day,
            'body_year': year_last2,
            'body_subcontractor_name': contractor_name,
            'body_company_name': company_name
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="lien_waiver_form.pdf"'
        formService = PDFFormFillService()
        response.write(formService.fill_form('PDF/COI/lien_waiver_form_generic.pdf', fields))

        return response
