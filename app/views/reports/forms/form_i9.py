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

        phone_number = 'N/A'
        if (len(person_info.phones)) > 0:
            phone_number = person_info.phones[0]['number']

        ssn_tokenized = person_info.get_ssn_tokenized()

        birth_date_text = ''
        if (person_info.birth_date):
            birth_date_text = person_info.birth_date.strftime('%m/%d/%Y')

        # Populate the form fields
        fields = {
            'form1[0].#subform[6].FamilyName[0]': person_info.last_name,
            'form1[0].#subform[6].GivenName[0]': person_info.first_name,
            'form1[0].#subform[6].OtherNamesUsed[0]': 'N/A',
            'form1[0].#subform[6].StreetNumberName[0]': person_info.get_full_street_address(),
            'form1[0].#subform[6].CityOrTown[0]': person_info.city,
            'form1[0].#subform[6].State[0]': person_info.state,
            'form1[0].#subform[6].ZipCode[0]': person_info.zipcode,
            'form1[0].#subform[6].DateOfBirth[0]': birth_date_text,
            'form1[0].#subform[6].SocialSecurityNumber1[0]': ssn_tokenized[0],
            'form1[0].#subform[6].SocialSecurityNumber2[0]': ssn_tokenized[1],
            'form1[0].#subform[6].SocialSecurityNumber3[0]': ssn_tokenized[2],
            'form1[0].#subform[6].email[0]': person_info.email,
            'form1[0].#subform[6].TelephoneNumber[0]': phone_number
        }

        if (i9_info):
            fields['form1[0].#subform[6].DateofSignaturebyEmployee[0]'] = i9_info.signature_date
            
            if (i9_info.citizen_data is not None):
                fields['form1[0].#subform[6].Checkbox1a[0]'] = 'Y'
            elif (i9_info.non_citizen_data is not None):
                fields['form1[0].#subform[6].Checkbox1b[0]'] = 'Y'
            elif (i9_info.perm_resident_data is not None):
                fields['form1[0].#subform[6].Checkbox1c[0]'] = 'Y'
                fields['form1[0].#subform[6].AlienNumber[0]'] = i9_info.perm_resident_data['uscis_number']
            elif (i9_info.authorized_worker_data is not None):
                fields['form1[0].#subform[6].Checkbox1d[0]'] = 'Y'
                fields['form1[0].#subform[6].ExpirationDate[0]'] = i9_info.authorized_worker_data['expiration_date']
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
                fields['form1[0].#subform[6].AlienNumber[1]'] = uscis_number
                fields['form1[0].#subform[6].I94Number[0]'] = i94_number
                fields['form1[0].#subform[6].PassportNumber[0]'] = passport_number
                fields['form1[0].#subform[6].CountryOfIssuance[0]'] = country_of_issuance

        file_name_prefix = ''
        full_name = person_info.get_full_name()
        if (full_name is not None):
            file_name_prefix = full_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_I9.pdf"'
        
        # Now produce the PDF with information filled
        formService = PDFFormFillService()
        pdf_stream = formService.get_filled_form_stream('PDF/i-9.pdf', fields)

        # Now utilize the signature service to apply the user's signature
        # if applicable
        signature_service = SignatureService()
        sign_success = signature_service.sign_pdf_stream(
            pk,
            pdf_stream,
            PdfFormSignaturePlacements.Form_I9,
            response
        )

        if (not sign_success):
            response.write(pdf_stream.read())

        return response
