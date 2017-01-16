
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

import xlwt

from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.models.employee_profile import EmployeeProfile
from app.models.health_benefits.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption
from app.models.health_benefits.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.health_benefits.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.health_benefits.enrolled import Enrolled
from app.models.health_benefits.benefit_plan import BenefitPlan
from app.models.health_benefits.benefit_type import BenefitType
from app.models.insurance.company_life_insurance_plan import CompanyLifeInsurancePlan
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from app.models.insurance.supplemental_life_insurance_plan import SupplementalLifeInsurancePlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import PersonCompSupplLifeInsurancePlan
from app.models.insurance.comp_suppl_life_insurance_plan import CompSupplLifeInsurancePlan
from app.models.insurance.supplemental_life_insurance_beneficiary import SupplementalLifeInsuranceBeneficiary
from app.models.insurance.std_insurance_plan import StdInsurancePlan
from app.models.insurance.company_std_insurance_plan import CompanyStdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan
from app.models.insurance.ltd_insurance_plan import LtdInsurancePlan
from app.models.insurance.company_ltd_insurance_plan import CompanyLtdInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.hra.hra_plan import HraPlan
from app.models.hra.company_hra_plan import CompanyHraPlan
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.fsa.fsa import FSA
from app.models.sys_benefit_update_reason import SysBenefitUpdateReason

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from ..excel_export_view_base import ExcelExportViewBase
from ..report_export_view_base import ReportExportViewBase

User = get_user_model()

class CompanyHphcExcelView(ExcelExportViewBase):

    def _write_headers(self):
        self._write_cell('SUBSCRIBER SSN')
        self._write_cell('MEMBER TITLE')
        self._write_cell('MEMBER FIRST NAME')
        self._write_cell('MEMBER MIDDLE INITIAL')
        self._write_cell('MEMBER LAST NAME')
        self._write_cell('MEMBER SUFFIX')
        self._write_cell('MEMBER DOB')
        self._write_cell('MEMBER SSN')
        self._write_cell('RELATIONSHIP TO SUBSCRIBER')
        self._write_cell('MEMBER GENDER')
        self._write_cell('MEMBER ADDRESS 1')
        self._write_cell('MEMBER ADDRESS 2')
        self._write_cell('MEMBER CITY')
        self._write_cell('MEMBER STATE')
        self._write_cell('MEMBER ZIP CODE')
        self._write_cell('MEMBER PHONE')
        self._write_cell('MEMBER E-MAIL')
        self._write_cell('CUSTOMER ACCOUNT NO')
        self._write_cell('HPHC PCP ID')
        self._write_cell('PCP FIRST NAME')
        self._write_cell('PCP LAST NAME')
        self._write_cell('PCP CITY')
        self._write_cell('MEMBER MEDICARE CLAIM NO')
        self._write_cell('MEMBER HOSPITAL PART A EFFECTIVE DATE')
        self._write_cell('MEDICARE MEDICAL PART B EFFECTIVE DATE')
        self._write_cell('PLAN OPTION')

    def _write_company(self, company_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(user_ids)):
            self._write_employee(user_ids[i])

        return

    def _write_employee(self, employee_user_id):
        self._write_employee_family_members(employee_user_id)
        return

    def _write_employee_family_members(self, employee_user_id):
        family_members = Person.objects.filter(user=employee_user_id)
        for member in family_members:
            self._write_employee_family_member(employee_user_id, member)

    def _write_employee_family_member(self, employee_user_id, family_person):
        # Only show members that are on the policy
        enrolled = None
        enrolleds = Enrolled.objects.filter(user_company_benefit_plan_option__benefit__benefit_plan__benefit_type__name='Medical', person=family_person.id)
        if (len(enrolleds) > 0):
            enrolled = enrolleds[0]
        else:
            return

        self._next_row()
        self._write_employee_personal_info(employee_user_id)
        self._write_person_basic_info(family_person)
        self._write_person_address_info(family_person)
        self._write_person_phone_info(family_person)
        self._write_person_email_info(family_person)
        self._write_person_plan_account_number(family_person)
        self._write_person_PCP_info(enrolled)
        self._write_person_medicare_info(family_person)
        self._write_person_plan_option_info(enrolled)

    def _write_employee_personal_info(self, employee_user_id):
        person = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]
            self._write_cell(person.ssn)
        else:
            self._skip_cells(1)

    def _write_person_basic_info(self, person_model):
        if (person_model):
            self._skip_cells(1)  # Title
            self._write_cell(person_model.first_name)
            self._skip_cells(1)  # Middle Initial
            self._write_cell(person_model.last_name)
            self._skip_cells(1)  # Suffix
            self._write_cell(ReportExportViewBase.get_date_string(person_model.birth_date))
            self._write_cell(person_model.ssn)
            self._write_cell(person_model.relationship.title())
            self._write_cell(person_model.gender)
        else:
            self._skip_cells(9)

    def _write_person_address_info(self, person_model):
        if (person_model):
            addresses = person_model.addresses.filter(address_type='home')
            if (len(addresses) > 0):
                address = addresses[0]
                self._write_cell(address.street_1)
                self._write_cell(address.street_2)
                self._write_cell(address.city)
                self._write_cell(address.state)
                self._write_cell(address.zipcode)
                return

        # Found no address, skip over the columns
        self._skip_cells(5)

    def _write_person_email_info(self, person_model):
        if (person_model):
            self._write_cell(person_model.email)
        else:
            self._skip_cells(1)

    def _write_person_phone_info(self, person_model):
        if (person_model):
            home_phones = person_model.phones.filter(phone_type='home')
            work_phones = person_model.phones.filter(phone_type='home')
            phone_num = None
            if(len(home_phones) > 0):
                phone_num = home_phones[0].number
            elif(len(work_phones) > 0):
                phone_num = work_phones[0].number
            self._write_cell(phone_num)
        else:
            self._skip_cells(1)

    def _write_person_plan_account_number(self, person_model):
        self._skip_cells(1)

    def _write_person_PCP_info(self, enrolled_model):
        self._write_cell(enrolled_model.pcp)
        # Skip PCP name and city for now
        self._skip_cells(3)

    def _write_person_medicare_info(self, person_model):
        self._skip_cells(3)

    def _write_person_plan_option_info(self, enrolled_model):
        self._write_cell(enrolled_model.user_company_benefit_plan_option.benefit.benefit_plan.name)

    # @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        self._init()
        self._start_work_sheet('Hphc Company Summary')

        self._write_headers()
        self._write_company(pk)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=hphc.xls'
        self._save(response)

        return response
