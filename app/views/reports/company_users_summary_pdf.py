from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Max
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.enrolled import Enrolled
from app.models.benefit_plan import BenefitPlan
from app.models.benefit_type import BenefitType
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
User = get_user_model()

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from pdf_export_view_base import PdfExportViewBase

class CompanyUsersSummaryPdfExportView(PdfExportViewBase):

    @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="employee_benefit_summary.pdf"'
        
        # initialize the canvas
        self._init_canvas(response)

        self._write_company(pk)

        self._save()

        return response

    def _write_company(self, company_id):
        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i])

        return

    def _write_employee(self, employee_user_id):
        person = self._get_person_by_user(employee_user_id)
        user = self._get_user_by_id(employee_user_id)

        # Write full name of the employee being rendered
        full_name = self._get_person_full_name(person, user)
        self._write_line([full_name])

        self._start_new_line()
        self._start_new_line()

        # Now starts writing benefit enrollments
        self._write_employee_all_health_benefits_info(user)

        # end the current page for the current employ
        # and start a new one for the next
        self._start_new_page()

        return

    def _write_employee_all_health_benefits_info(self, user_model):
        user_benefit_plan_options = UserCompanyBenefitPlanOption.objects.filter(user=user_model.id)
        user_benefit_waived = UserCompanyWaivedBenefit.objects.filter(user=user_model.id)

        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Medical')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Dental')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Vision')

        return

    def _write_employee_health_benefit_info(self, employee_health_benefit_options, employee_health_waived_benefit, benefit_type):
        # Render header
        self._write_line_uniform_width([benefit_type + ' Plan', 'Enrolled Members', 'Employee Premium'])
        self._draw_line()
        self._start_new_line()
        self._start_new_line()

        # user_benefit_options = employee_health_benefit_options.filter(benefit__benefit_plan__benefit_type__name = benefit_type)
        # user_waived_benefit = employee_health_waived_benefit.filter(benefit_type__name = benefit_type)

        # if len(user_benefit_options) > 0:
        #     user_benefit_option = user_benefit_options[0]
        #     company_plan_option = user_benefit_option.benefit
        #     benefit_plan = company_plan_option.benefit_plan
        #     col_num = self._write_field(excelSheet, row_num, col_num, benefit_plan.name)
        #     col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.benefit_option_type)
        #     if benefit_type == 'Medical':
        #         col_num = col_num + 2
        #     else:
        #         col_num = col_num + 1
        #     col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.employee_cost_per_period)
        #     col_num = self._write_employee_benefit_record_reason(user_benefit_option, excelSheet, row_num, col_num)
        #     return col_num

        # elif len(user_waived_benefit) > 0:
        #     user_waived = user_waived_benefit[0]
        #     col_num = col_num + 2
        #     col_num = self._write_field(excelSheet, row_num, col_num, "Waived")
        #     if benefit_type == 'Medical':
        #         col_num = self._write_field(excelSheet, row_num, col_num, user_waived.reason)
        #     col_num = self._write_field(excelSheet, row_num, col_num, "0")
        #     col_num = self._write_employee_benefit_record_reason(user_waived, excelSheet, row_num, col_num)
        #     return col_num

        return

    def _get_person_full_name(self, person_model, fallback_user=None):
        full_name = 'N/A'

        if (person_model):
            full_name = self._concat_strings([person_model.first_name, person_model.middle_name, person_model.last_name])
        elif (fallback_user):
            full_name = self._concat_strings([fallback_user.first_name, fallback_user.last_name])

        if (len(full_name) <= 0):
            full_name = 'N/A'

        return full_name

    def _get_person_by_user(self, user_id):
        person = None
        persons = Person.objects.filter(user=user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]
        return person

    def _get_user_by_id(self, user_id):
        user = None
        users = User.objects.filter(pk=user_id)
        if (len(users) > 0):
            user = users[0]
        return user

    def _concat_strings(self, strings, delim=' '):
        result = ''
        for string in strings:
            if string is not None:
                if len(result) > 0:
                    result = result + delim
                result = result + string

        return result


    def _check_None(self, target, default_value):
        return target if target is not None else default_value

