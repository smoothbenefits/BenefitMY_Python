from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase

User = get_user_model()


class Form1095CView(ReportExportViewBase):

    def get(self, request, pk, format=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="1095-C.pdf"'

        # Populate the form fields
        fields = {
            # Name Employee
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_002[0]': '1',
            # SSN
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_003[0]': '2',
            # Street Address
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_004[0]': '3',
            # City
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_005[0]': '4',
            # State
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_006[0]': '5',
            # Country and Zip or Foreign Postcode
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_007[0]': '6',

            # Name Employer
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_008[0]': '7',
            # EIN
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_009[0]': '8',
            # Street Address
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_010[0]': '9',
            # Contact Phone Number
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_011[0]': '10',
            # City
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_012[0]': '11',
            # State
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_013[0]': '12',
            # Country and Zip or Foreign Postcode
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_014[0]': '13',
        }

        formService = PDFFormFillService()
        formService.fill_form('PDF/1095c.pdf', fields, response)

        return response
