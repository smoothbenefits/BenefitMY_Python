from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

import xlwt

from app.models.person import Person
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.company_life_insurance_plan import CompanyLifeInsurancePlan
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from app.models.insurance.supplemental_life_insurance_plan import SupplementalLifeInsurancePlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import PersonCompSupplLifeInsurancePlan
from app.models.insurance.comp_suppl_life_insurance_plan import CompSupplLifeInsurancePlan
from app.models.insurance.supplemental_life_insurance_beneficiary import SupplementalLifeInsuranceBeneficiary

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from company_users_full_summary_excel import CompanyUsersFullSummaryExcelExportView

User = get_user_model()

class CompanyUsersLifeInsuranceBeneficiaryExcelExportView(CompanyUsersFullSummaryExcelExportView):
    def _write_headers(self, excelSheet):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Birth Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Date of Hire')
        col_num = self._write_field(excelSheet, 0, col_num, 'Email')
        col_num = self._write_field(excelSheet, 0, col_num, 'Work Phone')
        col_num = self._write_field(excelSheet, 0, col_num, 'Home Phone')
        col_num = self._write_field(excelSheet, 0, col_num, 'Address 1')
        col_num = self._write_field(excelSheet, 0, col_num, 'Address 2')
        col_num = self._write_field(excelSheet, 0, col_num, 'City')
        col_num = self._write_field(excelSheet, 0, col_num, 'State')
        col_num = self._write_field(excelSheet, 0, col_num, 'Zip')

        for i in range(0, 4):
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Middle Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Relationship ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Email ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Phone ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Beneficiary Percentage ' + `i+1`)

        for i in range(0, 4):
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Middle Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Relationship ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Email ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Phone ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Contingent Beneficiary Percentage ' + `i+1`)

        for i in range(0, 4):
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Middle Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Relationship ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Email ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Phone ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Beneficiary Percentage ' + `i+1`)

        for i in range(0, 4):
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Middle Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Relationship ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Email ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Phone ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Supplemental Life Contingent Beneficiary Percentage ' + `i+1`)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_column_num = 0
        start_column_num = self._write_employee_personal_info(employee_user_id, False, False, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_basic_life_insurance_beneficiary_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_supplemental_life_insurance_beneficiary_info(employee_user_id, excelSheet, row_num, start_column_num)
        return

    def _write_employee_basic_life_insurance_beneficiary_info(self, employee_user_id, excelSheet, row_num, col_num):
        col_num = self._write_employee_basic_life_insurance_beneficiary_info_by_tier(employee_user_id, 1, excelSheet, row_num, col_num)
        col_num = self._write_employee_basic_life_insurance_beneficiary_info_by_tier(employee_user_id, 2, excelSheet, row_num, col_num)
        return col_num

    def _write_employee_basic_life_insurance_beneficiary_info_by_tier(self, employee_user_id, beneficiary_tier, excelSheet, row_num, col_num):
        beneficiary_set = [None] * 4
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = UserCompanyLifeInsurancePlan.objects.filter(person=employee_person.id).filter(company_life_insurance__life_insurance_plan__insurance_type='Basic')
            if (len(employee_plans) > 0):
                employee_plan = employee_plans[0]
                beneficiaries = employee_plan.life_insurance_beneficiary.filter(tier=beneficiary_tier)
                for i in range(0, min(len(beneficiaries), 4)):
                    beneficiary_set[i] = beneficiaries[i]

        for i in range(0, len(beneficiary_set)):
            col_num = self._write_beneficiary_info(beneficiary_set[i], excelSheet, row_num, col_num)

        return col_num

    def _write_employee_supplemental_life_insurance_beneficiary_info(self, employee_user_id, excelSheet, row_num, col_num):
        col_num = self._write_employee_supplemental_life_insurance_beneficiary_info_by_tier(employee_user_id, 1, excelSheet, row_num, col_num)
        col_num = self._write_employee_supplemental_life_insurance_beneficiary_info_by_tier(employee_user_id, 2, excelSheet, row_num, col_num)
        return col_num

    def _write_employee_supplemental_life_insurance_beneficiary_info_by_tier(self, employee_user_id, beneficiary_tier, excelSheet, row_num, col_num):
        beneficiary_set = [None] * 4
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = PersonCompSupplLifeInsurancePlan.objects.filter(person=employee_person.id)
            if (len(employee_plans) > 0):
                employee_plan = employee_plans[0]
                beneficiaries = employee_plan.suppl_life_insurance_beneficiary.filter(tier=beneficiary_tier)
                for i in range(0, min(len(beneficiaries), 4)):
                    beneficiary_set[i] = beneficiaries[i]

        for i in range(0, len(beneficiary_set)):
            col_num = self._write_beneficiary_info(beneficiary_set[i], excelSheet, row_num, col_num)

        return col_num

    def _write_beneficiary_info(self, beneficiary_model, excelSheet, row_num, col_num):
        if (beneficiary_model):
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.last_name)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.relationship)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.email)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.phone)
            col_num = self._write_field(excelSheet, row_num, col_num, beneficiary_model.percentage)
            return col_num

        return col_num + 7

    ''' Both broker and employer should be able to get summary of beneficiary
        information about employees
    '''
    @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('All Employee Summary')

        self._write_headers(sheet)

        self._write_company(pk, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=employee_life_beneficiary_summary.xls'
        book.save(response)
        return response
