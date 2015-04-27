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
from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.company_life_insurance_plan import CompanyLifeInsurancePlan
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from app.models.insurance.std_insurance_plan import StdInsurancePlan
from app.models.insurance.company_std_insurance_plan import CompanyStdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan
from app.models.insurance.ltd_insurance_plan import LtdInsurancePlan
from app.models.insurance.company_ltd_insurance_plan import CompanyLtdInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.fsa import FSA
from app.models.direct_deposit import DirectDeposit
from app.models.user_bank_account import UserBankAccount
from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)

User = get_user_model()

class ExportViewBase(APIView):
    def _get_max_dependents_count(self, company_id):
        users_id = self._get_all_employee_user_ids_for_company(company_id)
        persons = Person.objects.filter(user__in=users_id).exclude(relationship='self').exclude(relationship='spouse')

        # persons.groupby('user').count('pk').max()
        max_dependents = persons.values('user').annotate(num_dependents=Count('pk')).aggregate(max=Max('num_dependents'))

        result = max_dependents['max']

        if (result):
            return result

        return 0

    def _get_max_direct_deposit_count(self, company_id):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)
        direct_deposits = DirectDeposit.objects.filter(user__in=user_ids)
        max_direct_deposits = direct_deposits.values('user').annotate(num_direct_deposit=Count('pk')).aggregate(max=Max('num_direct_deposit'))

        result = max_direct_deposits['max']
        if (result):
            return result
        return 0

    def _get_all_employee_user_ids_for_company(self, company_id):
        # Get all employees for the company
        users_id = []
        users = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for user in users:
            users_id.append(user.user_id)

        return users_id

class ExcelExportViewBase(ExportViewBase):
    date_field_format = xlwt.XFStyle()
    date_field_format.num_format_str= 'mm-dd-yyyy'

    ''' Sadly Python does not support the ++ operator, or else we don't need
        this below helper to keep track of the next column number for writing
        individule field
    '''
    def _write_field(self, excelSheet, row_num, col_num, value, value_format=None):
        if (value_format):
            excelSheet.write(row_num, col_num, value, value_format)
        else:
            excelSheet.write(row_num, col_num, value)
        return col_num + 1

class CompanyUsersDirectDepositExcelExportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet, max_direct_deposits):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')

        for i in range(max_direct_deposits):
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Type ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Issurer ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Routing Number ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Account Number ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Attachment URL ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Remainder of Net Pay' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Amount ' + str(i + 1))
            col_num = self._write_field(excelSheet, 0, col_num, 'Percentage ' + str(i + 1))

        return

    def _write_company(self, company_id, excelSheet):
        user_ids = self._get_all_employee_user_ids_for_company(company_id)

        # for each employee, write direct deposit for him/her
        for i in range(len(user_ids)):
            self._write_employee(user_ids[i], excelSheet, i + 1)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_col_num = 0
        start_col_num = self._write_employee_personal_info(employee_user_id, excelSheet, row_num, start_col_num)
        start_col_num = self._write_employee_direct_deposit(employee_user_id, excelSheet, row_num, start_col_num)
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

        return cur_column_num

    def _write_person_basic_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
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
                col_num = self._write_field(excelSheet, row_num, col_num, user.first_name)
                col_num = self._write_field(excelSheet, row_num, col_num, None)
                col_num = self._write_field(excelSheet, row_num, col_num, user.last_name)

                # now skip 3 more columns to align with the normal person profile output
                return col_num + 3

        # Skip the columns
        return col_num + 6

    def _write_employee_direct_deposit(self, employee_user_id, excelSheet, row_num, start_col_num):
        current_col_num = start_col_num

        direct_deposit = None
        direct_deposits = DirectDeposit.objects.filter(user_id=employee_user_id)

        for i in range(len(direct_deposits)):
            current_col_num = self._write_direct_deposit(direct_deposits[i], excelSheet, row_num, current_col_num)

        return current_col_num

    def _write_direct_deposit(self, direct_deposit, excelSheet, row_num, start_col_num):
        current_col_num = start_col_num

        # each direct deposit has only one bank account
        user_bank_account = UserBankAccount.objects.filter(pk=direct_deposit.bank_account.id)[0]

        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.account_type)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.bank_name)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.routing)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.account)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, user_bank_account.attachment)

        is_ronp = 'Yes' if direct_deposit.remainder_of_all else 'No'

        current_col_num = self._write_field(excelSheet, row_num, current_col_num, is_ronp)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, direct_deposit.amount)
        current_col_num = self._write_field(excelSheet, row_num, current_col_num, direct_deposit.percentage)

        return current_col_num

    ''' Direct Deposit summary is expected to be visible to employer only
        Broker should not need such inforation
    '''
    @user_passes_test(company_employer)
    def get(self, request, pk, format=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('Direct Deposit')

        # Pre compute the max number of dependents across all employees of
        # the company, so we know how many sets of headers for dependent
        # info we need to populate
        max_direct_deposits = self._get_max_direct_deposit_count(pk)
        self._write_headers(sheet, max_direct_deposits)

        self._write_company(pk, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=employee_direct_deposit.xls'
        book.save(response)
        return response

class CompanyUsersSummaryExcelExportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet, max_dependents):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Birth Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Email')
        col_num = self._write_field(excelSheet, 0, col_num, 'Work Phone')
        col_num = self._write_field(excelSheet, 0, col_num, 'Home Phone')
        col_num = self._write_field(excelSheet, 0, col_num, 'Address 1')
        col_num = self._write_field(excelSheet, 0, col_num, 'Address 2')
        col_num = self._write_field(excelSheet, 0, col_num, 'City')
        col_num = self._write_field(excelSheet, 0, col_num, 'State')
        col_num = self._write_field(excelSheet, 0, col_num, 'Zip')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Birth Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Relationship')

        col_num = self._write_field(excelSheet, 0, col_num, 'Med Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Cost / Pay')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Cost / Pay')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Cost / Pay')

        col_num = self._write_field(excelSheet, 0, col_num, 'STD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Amount')

        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Amount')

        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Amount')

        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optionak Life Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optionak Life Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optionak Life Amount')

        col_num = self._write_field(excelSheet, 0, col_num, 'FSA Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dependent FSA Amount')

        for i in range(0, max_dependents):
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Middle Initial ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep SSN ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Gender ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Birth Date ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Relationship ' + `i+1`)

        return

    def _write_company(self, company_id, excelSheet):
        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], excelSheet, i + 1)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_column_num = 0
        start_column_num = self._write_employee_personal_info(employee_user_id, True, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_all_health_benefits_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_std_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_ltd_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_basic_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_supplemental_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_fsa_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_all_dependents_personal_info(employee_user_id, excelSheet, row_num, start_column_num)
        return

    def _write_employee_personal_info(self, employee_user_id, include_spouse_info, excelSheet, row_num, start_column_num):
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

        # Write out phone number info
        cur_column_num = self._write_person_phone_info(person, 'work', excelSheet, row_num, cur_column_num)
        cur_column_num = self._write_person_phone_info(person, 'home', excelSheet, row_num, cur_column_num)

        # Write out address info
        cur_column_num = self._write_person_address_info(person, 'home', excelSheet, row_num, cur_column_num)

        # Write spouse personal_info
        if (include_spouse_info):
            cur_column_num = self._write_spouse_personal_info(person, excelSheet, row_num, cur_column_num)

        return cur_column_num

    def _write_person_basic_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.ssn)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.gender)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.birth_date, ExcelExportViewBase.date_field_format)
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
                col_num = self._write_field(excelSheet, row_num, col_num, user.first_name)
                col_num = self._write_field(excelSheet, row_num, col_num, None)
                col_num = self._write_field(excelSheet, row_num, col_num, user.last_name)

                # now skip 3 more columns to align with the normal person profile output
                return col_num + 3

        # Skip the columns
        return col_num + 6

    def _write_person_email_info(self, person_model, excelSheet, row_num, col_num, employee_user_id = None):
        if (person_model):
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

    def _write_person_phone_info(self, person_model, phone_type, excelSheet, row_num, col_num):
        if (person_model):
            phones = person_model.phones.filter(phone_type=phone_type)
            phone_num = None
            if(len(phones) > 0):
                phone_num = phones[0].number
            return self._write_field(excelSheet, row_num, col_num, phone_num)
        return col_num + 1

    def _write_person_address_info(self, person_model, address_type, excelSheet, row_num, col_num):
        if (person_model):
            addresses = person_model.addresses.filter(address_type=address_type)
            if (len(addresses) > 0):
                address = addresses[0]
                col_num = self._write_field(excelSheet, row_num, col_num, address.street_1)
                col_num = self._write_field(excelSheet, row_num, col_num, address.street_2)
                col_num = self._write_field(excelSheet, row_num, col_num, address.city)
                col_num = self._write_field(excelSheet, row_num, col_num, address.state)
                col_num = self._write_field(excelSheet, row_num, col_num, address.zipcode)
                return col_num

        # Found no address, skip over the columns
        return col_num + 5

    def _write_spouse_personal_info(self, person_model, excelSheet, row_num, col_num):
        family_members = Person.objects.none()
        if (person_model):
            family_members = Person.objects.filter(user=person_model.user).filter(relationship='spouse')

        spouse = None
        if (len(family_members) > 0):
            spouse = family_members[0]
        col_num = self._write_family_member_personal_info(spouse, excelSheet, row_num, col_num)

        return col_num

    def _write_all_dependents_personal_info(self, employee_user_id, excelSheet, row_num, col_num):
        persons = Person.objects.filter(user=employee_user_id)
        person_model = None
        if (len(persons) > 0):
            person_model = persons[0]

        family_members = Person.objects.none()
        if (person_model):
            family_members = Person.objects.filter(user=person_model.user).exclude(relationship='self').exclude(relationship='spouse')

        for member in family_members:
            col_num = self._write_family_member_personal_info(member, excelSheet, row_num, col_num)

        return col_num

    def _write_family_member_personal_info(self, family_person_model, excelSheet, row_num, col_num):
        col_num = self._write_person_basic_info(family_person_model, excelSheet, row_num, col_num)

        if (family_person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, family_person_model.relationship)
            return col_num

        # Skip the relationship column
        return col_num + 1

    def _write_employee_all_health_benefits_info(self, employee_user_id, excelSheet, row_num, col_num):
        user_benefit_plan_options = UserCompanyBenefitPlanOption.objects.filter(user=employee_user_id)

        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, 'Medical', excelSheet, row_num, col_num)
        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, 'Dental', excelSheet, row_num, col_num)
        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, 'Vision', excelSheet, row_num, col_num)

        return col_num

    def _write_employee_health_benefit_info(self, employee_health_benefit_options, benefit_type, excelSheet, row_num, col_num):
        user_benefit_options = employee_health_benefit_options.filter(benefit__benefit_plan__benefit_type__name=benefit_type)

        if (len(user_benefit_options) > 0):
            user_benefit_option = user_benefit_options[0]
            company_plan_option = user_benefit_option.benefit
            benefit_plan = company_plan_option.benefit_plan

            col_num = self._write_field(excelSheet, row_num, col_num, benefit_plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.benefit_option_type)
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.employee_cost_per_period)

            return col_num

        # Skip the columns if no matching benefit
        return col_num + 3

    def _write_employee_std_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyStdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_std_insurance
            plan = company_plan.std_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, str(company_plan.percentage_of_salary) + '% of Salary')

            return col_num

        return col_num + 2

    def _write_employee_ltd_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLtdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_ltd_insurance
            plan = company_plan.ltd_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, str(company_plan.percentage_of_salary) + '% of Salary')

            return col_num

        return col_num + 2

    def _write_employee_basic_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=employee_user_id).filter(company_life_insurance__life_insurance_plan__insurance_type='Basic')
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_life_insurance
            plan = company_plan.life_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan.insurance_amount)

            return col_num

        return col_num + 2

    def _write_employee_supplemental_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=employee_user_id).filter(company_life_insurance__life_insurance_plan__insurance_type='Extended')
        col_num = self._write_family_member_supplemental_life_insurance_info(employee_user_id, 'self', employee_plans, excelSheet, row_num, col_num)
        col_num = self._write_family_member_supplemental_life_insurance_info(employee_user_id, 'spouse', employee_plans, excelSheet, row_num, col_num)
        col_num = self._write_family_member_supplemental_life_insurance_info(employee_user_id, 'dependent', employee_plans, excelSheet, row_num, col_num)

        return col_num

    def _write_family_member_supplemental_life_insurance_info(self, employee_user_id, member_relationship, family_member_plans, excelSheet, row_num, col_num):
        members = Person.objects.filter(user=employee_user_id).filter(relationship=member_relationship)
        if (len(members) > 0):
            member = members[0]
            plans = family_member_plans.filter(person=member.id)
            if (len(plans) > 0):
                plan = plans[0]
                col_num = self._write_field(excelSheet, row_num, col_num, plan.company_life_insurance.life_insurance_plan.name)
                col_num = self._write_field(excelSheet, row_num, col_num, plan.insurance_amount)
                return col_num

        return col_num + 2 

    def _write_employee_fsa_info(self, employee_user_id, excelSheet, row_num, col_num):
        fsas = FSA.objects.filter(user=employee_user_id)
        if (len(fsas) > 0):
            fsa = fsas[0]
            col_num = self._write_field(excelSheet, row_num, col_num, fsa.primary_amount_per_year)
            col_num = self._write_field(excelSheet, row_num, col_num, fsa.dependent_amount_per_year)
            return col_num

        return col_num + 2

    ''' Both broker and employer should be able to get summary of all 
        benefit situations of all employees of the company
    '''
    @user_passes_test(company_employer_or_broker)
    def get(self, request, pk, format=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('All Employee Summary')

        # Pre compute the max number of dependents across all employees of
        # the company, so we know how many sets of headers for dependent
        # info we need to populate
        max_dependents = self._get_max_dependents_count(pk)
        self._write_headers(sheet, max_dependents)

        self._write_company(pk, sheet)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=employee_summary.xls'
        book.save(response)
        return response


class CompanyUsersLifeInsuranceBeneficiaryExcelExportView(CompanyUsersSummaryExcelExportView):
    def _write_headers(self, excelSheet):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Birth Date')
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
        start_column_num = self._write_employee_personal_info(employee_user_id, False, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_life_insurance_beneficiary_info(employee_user_id, 'Basic', excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_life_insurance_beneficiary_info(employee_user_id, 'Extended', excelSheet, row_num, start_column_num)
        return

    def _write_employee_life_insurance_beneficiary_info(self, employee_user_id, life_insurance_plan_type, excelSheet, row_num, col_num):
        col_num = self._write_employee_life_insurance_beneficiary_info_by_tier(employee_user_id, life_insurance_plan_type, 1, excelSheet, row_num, col_num)
        col_num = self._write_employee_life_insurance_beneficiary_info_by_tier(employee_user_id, life_insurance_plan_type, 2, excelSheet, row_num, col_num)
        return col_num

    def _write_employee_life_insurance_beneficiary_info_by_tier(self, employee_user_id, life_insurance_plan_type, beneficiary_tier, excelSheet, row_num, col_num):
        beneficiary_set = [None] * 4
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = UserCompanyLifeInsurancePlan.objects.filter(person=employee_person.id).filter(company_life_insurance__life_insurance_plan__insurance_type=life_insurance_plan_type)
            if (len(employee_plans) > 0):
                employee_plan = employee_plans[0]
                beneficiaries = employee_plan.life_insurance_beneficiary.filter(tier=beneficiary_tier)
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
