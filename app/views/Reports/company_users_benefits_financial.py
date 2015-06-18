import xlwt
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.db.models import Count, Max
from django.contrib.auth import get_user_model
from ..company_user_summary_view import ExcelExportViewBase
from app.models.person import Person
from app.models.company import Company
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
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
from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)

User = get_user_model()

class CompanyUsersBenefitsFinancialExcelExportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Email')


        col_num = self._write_field(excelSheet, 0, col_num, 'STD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD total premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD employer premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD employee premium per period')

        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD total premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD employer premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD employee premium per period')

        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) total premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) employer premium per period')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) employee premium per period')

        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life total Premium per month')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Premium per Month')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Premium per Month')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Total Premium per Month')

        return

    def _write_company(self, company_id, excelSheet):
        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], excelSheet, i + 1)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_column_num = 0
        start_column_num = self._write_employee_personal_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_std_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_ltd_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_basic_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_supplemental_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        return

    def _write_employee_personal_info(self, employee_user_id, excelSheet, row_num, start_column_num):
        cur_column_num = start_column_num

        person = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]

        # All helpers are built with capability of skiping proper number of columns when
        # person given is None. This is to ensure other information written after these
        # would be written to the right columns
        cur_column_num = self._write_person_basic_info(person, excelSheet, row_num, cur_column_num, employee_user_id)
        cur_column_num = self._write_person_email_info(person, excelSheet, row_num, cur_column_num, employee_user_id)

        return cur_column_num

    def _write_person_basic_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
        elif (employee_user_id):
            # TODO:
            # This is not a clean solution, but is the only one we have for the short term
            # The desire is to also include some basic information for an employee, even if
            # he has not gone through on-boarding yet
            # So without the person profile that is filled out during onboarding, all we can
            # do for now is to grab the basic information from the user account.
            users = User.objects.filter(pk=employee_user_id)
            if (len(users) > 0):
                user = users[0]
                col_num = self._write_field(excelSheet, row_num, col_num, user.first_name)
                col_num = self._write_field(excelSheet, row_num, col_num, None)
                col_num = self._write_field(excelSheet, row_num, col_num, user.last_name)
        else:
            # Skip the columns
            col_num = col_num + 3
        
        return col_num

    def _write_person_email_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model and person_model.email):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.email)
            return col_num
        elif (employee_user_id):
            # TODO:
            # This is not a clean solution, but is the only one we have for the short term
            # The desire is to also include some basic information for an employee, even if
            # he has not gone through on-boarding yet
            # So without the person profile that is filled out during onboarding, all we can
            # do for now is to grab the basic information from the user account.
            users = User.objects.filter(pk=employee_user_id)
            if (len(users) > 0):
                user = users[0]
                col_num = self._write_field(excelSheet, row_num, col_num, user.email)
                return col_num

        return col_num + 1


    def _write_employee_std_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyStdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_std_insurance
            plan = company_plan.std_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            employee_premium = employee_plan.total_premium_per_period or 0
            employer_contribution = company_plan.employer_contribution_percentage or 0
            total_premium = float(employee_premium) * 100 / (100 - float(employer_contribution))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(total_premium))
            employer_premium = total_premium - float(employee_premium)
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employer_premium))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employee_premium))

            return col_num

        return col_num + 4

    def _write_employee_ltd_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLtdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_ltd_insurance
            plan = company_plan.ltd_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            employee_premium = employee_plan.total_premium_per_period or 0
            employer_contribution = company_plan.employer_contribution_percentage or 0
            total_premium = float(employee_premium) * 100 / (100 - float(employer_contribution))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(total_premium))
            employer_premium = total_premium - float(employee_premium)
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employer_premium))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employee_premium))

            return col_num

        return col_num + 4

    def _write_employee_basic_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=employee_user_id).filter(company_life_insurance__life_insurance_plan__insurance_type='Basic')
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_life_insurance
            plan = company_plan.life_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            total_premium = company_plan.total_cost_per_period or 0
            employee_premium = company_plan.employee_cost_per_period or 0
            employer_premium = total_premium - employee_premium or 0
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(total_premium))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employer_premium))
            col_num = self._write_field(excelSheet, row_num, col_num, '{0:.2f}'.format(employee_premium))

            return col_num

        return col_num + 4

    def _write_employee_supplemental_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = PersonCompSupplLifeInsurancePlan.objects.filter(person=employee_person.id)
            if (len(employee_plans) > 0):
                plan = employee_plans[0]
                # Employee
                col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                self_premium = plan.self_premium_per_month or 0
                col_num = self._write_field(excelSheet, row_num, col_num, self_premium)
                # Spouse
                col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                spouse_premium = plan.spouse_premium_per_month or 0
                col_num = self._write_field(excelSheet, row_num, col_num, spouse_premium)
                # Child
                col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                child_premium = plan.child_premium_per_month or 0
                col_num = self._write_field(excelSheet, row_num, col_num, child_premium)
                total_premium = self_premium + spouse_premium + child_premium
                col_num = self._write_field(excelSheet, row_num, col_num, total_premium)
                return col_num
        return col_num + 7


    def _get_company_info(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    ''' Both broker and employer should be able to get summary of all 
        benefit situations of all employees of the company
    '''
    @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        comp = self._get_company_info(pk)
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Employee view')

        # Pre compute the max number of dependents across all employees of
        # the company, so we know how many sets of headers for dependent
        # info we need to populate
        max_dependents = self._get_max_dependents_count(pk)
        self._write_headers(sheet)

        self._write_company(pk, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        # Need company name:

        response['Content-Disposition'] = 'attachment; filename={0}_employee_benefits_financial.xls'.format(comp)
        book.save(response)
        return response
