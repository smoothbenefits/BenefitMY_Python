import StringIO
import cairosvg

from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.models.signature import Signature
from app.service.Report.pdf_form_fill_service import PDFFormFillService
from app.service.signature_service import (
    SignatureService,
    PdfFormSignaturePlacements
)
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from datetime import date, timedelta
from django.http import Http404

User = get_user_model()


class FormI9View(ReportExportViewBase):

    def get(self, request, pk, format=None):

        employee_user_id = pk
        model_factory = ReportViewModelFactory()
        person_info = model_factory.get_employee_person_info(employee_user_id)
        company_info = model_factory.get_employee_company_info(employee_user_id)
        i9_info = model_factory.get_employee_i9_data(employee_user_id)
        employee_profile_info = model_factory.get_employee_employment_profile_data(employee_user_id, company_info.company_id)

        phone_number = 'N/A'
        if (len(person_info.phones)) > 0:
            phone_number = person_info.phones[0]['number']

        ssn_tokenized = person_info.get_ssn_tokenized()

        birth_date_text = ''
        if (person_info.birth_date):
            birth_date_text = person_info.birth_date.strftime('%m/%d/%Y')

        # Populate the form fields
        fields = {
            'employee_last_name': person_info.last_name,
            'employee_first_name': person_info.first_name,
            'employee_other_last_name': 'N/A',
            'employee_address': person_info.get_full_street_address(),
            'employee_city': person_info.city,
            'employee_state': person_info.state,
            'employee_zip_code': person_info.zipcode,
            'employee_birth_date': birth_date_text,
            'employee_ssn_1': ssn_tokenized[0],
            'employee_ssn_2': ssn_tokenized[1],
            'employee_ssn_3': ssn_tokenized[2],
            'employee_email': person_info.email,
            'employee_phone': phone_number
        }

        s2_employee_status = ''

        if (i9_info):

            if (i9_info.citizen_data is not None):
                fields['employee_status_citizen'] = 'Yes'
                s2_employee_status = 1
            elif (i9_info.non_citizen_data is not None):
                fields['employee_status_non_citizen'] = 'Yes'
                s2_employee_status = 2
            elif (i9_info.perm_resident_data is not None):
                fields['employee_status_perm'] = 'Yes'
                fields['employee_perm_uscis_number'] = i9_info.perm_resident_data['uscis_number']
                s2_employee_status = 3
            elif (i9_info.authorized_worker_data is not None):
                fields['employee_status_alien'] = 'Yes'
                fields['employee_authorization_expire_date'] = i9_info.authorized_worker_data['expiration_date']
                uscis_number = ''
                i94_number = ''
                passport_number = ''
                country_of_issuance = ''
                if (i9_info.authorized_worker_data['uscis_number']):
                    uscis_number = i9_info.authorized_worker_data['uscis_number']
                else:
                    i94_number = i9_info.authorized_worker_data['i94_number']
                    passport_number = i9_info.authorized_worker_data['passport_number']
                    country_of_issuance = i9_info.authorized_worker_data['country_of_issuance'] 
                fields['employee_alien_uscis_number'] = uscis_number
                fields['employee_alien_i94'] = i94_number
                fields['employee_alien_passport'] = passport_number
                fields['employee_alien_passport_country'] = country_of_issuance
                s2_employee_status = 4

        # Section 2
        fields['s2_employee_last_name'] = person_info.last_name
        fields['s2_employee_first_name'] = person_info.first_name
        fields['s2_employee_status'] = s2_employee_status

        if (company_info):
            fields['employer_company_name'] = company_info.company_name
            fields['employer_company_address'] = company_info.get_full_street_address()
            fields['employer_company_city'] = company_info.city
            fields['employer_company_state'] = company_info.state
            fields['employer_company_zip_code'] = company_info.zipcode

        if (employee_profile_info):
            if (employee_profile_info.hire_date):
                fields['employment_start_date'] = employee_profile_info.hire_date.strftime('%m/%d/%Y')

        file_name_prefix = ''
        full_name = person_info.get_full_name()
        if (full_name is not None):
            file_name_prefix = full_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_I9.pdf"'
        
        # Now produce the PDF with information filled
        formService = PDFFormFillService()
        pdf_stream = formService.get_filled_form_stream('PDF/i-9.pdf', fields)

        response.write(pdf_stream.read())

        return response
