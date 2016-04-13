from django.http import HttpResponse
from django.http import Http404

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ...report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory


class FormLienWaiverView(ReportExportViewBase):

    def get(self, request, format=None):

        # Populate the form fields
        fields = {
            'topmostSubform[0].Page1[0].body_month[0]': 'March',
            'topmostSubform[0].Page1[0].body_day[0]': '02',
            'topmostSubform[0].Page1[0].body_year[0]': '16',
            'topmostSubform[0].Page1[0].body_subcontractor_name[0]': 'Ironman Construction',
            'topmostSubform[0].Page1[0].subcontractor_signature[0]': 'Alibaba Wahaha',
            'topmostSubform[0].Page1[0].subcontractor_date[0]': '03/02/2016',
            'topmostSubform[0].Page1[0].subcontractor_name[0]': 'Alibaba Wahaha',
            'topmostSubform[0].Page1[0].company_signature[0]': 'Batman Super',
            'topmostSubform[0].Page1[0].company_date[0]': '03/03/2016',
            'topmostSubform[0].Page1[0].company_title[0]': 'CEO'
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="lien_waiver_form.pdf"'
        formService = PDFFormFillService()
        formService.fill_form('PDF/COI/lien_waiver_form.pdf', fields, response)

        return response
