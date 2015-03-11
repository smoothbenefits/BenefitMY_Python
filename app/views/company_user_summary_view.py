from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction

import xlwt

from app.models.company_user import CompanyUser
from app.models.person import Person
from app.models.phone import Phone
from app.models.address import Address
from app.models.user import User
from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.company_life_insurance_plan import CompanyLifeInsurancePlan
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from app.models.fsa import FSA

class CompanyUsersSummaryExcelExportView(APIView):

    date_field_format = xlwt.XFStyle()
    date_field_format.num_format_str= 'mm-dd-yyyy'

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
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Birth Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Relationship')

        for i in range(0, 10):
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Middle Initial ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep SSN ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Gender ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Birth Date ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Relationship ' + `i+1`)

        col_num = self._write_field(excelSheet, 0, col_num, 'Med Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Cost / Pay')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Cost / Pay')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Cost / Pay')

        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Amount')

        return

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

    def _write_company(self, company_id, excelSheet):
        # Get all employees for the company
        users_id = []
        users = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for user in users:
            users_id.append(user.user_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], excelSheet, i + 1)

        return

    def _write_employee(self, employee_user_id, excelSheet, row_num):
        start_column_num = 0
        start_column_num = self._write_employee_personal_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_all_health_benefits_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_basic_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_optional_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_fsa_info(employee_user_id, excelSheet, row_num, start_column_num)
        return

    def _write_employee_personal_info(self, employee_user_id, excelSheet, row_num, start_column_num):
        cur_column_num = start_column_num
        try:
            person = Person.objects.get(user=employee_user_id, relationship='self')
            cur_column_num = self._write_person_basic_info(person, excelSheet, row_num, cur_column_num)
            cur_column_num = self._write_field(excelSheet, row_num, cur_column_num, person.email)

            # Write out phone number info
            cur_column_num = self._write_person_phone_info(person, 'work', excelSheet, row_num, cur_column_num)
            cur_column_num = self._write_person_phone_info(person, 'home', excelSheet, row_num, cur_column_num)

            # Write out address info
            cur_column_num = self._write_person_address_info(person, 'home', excelSheet, row_num, cur_column_num)

            # Write family personal_info
            cur_column_num = self._write_all_family_members_personal_info(person, excelSheet, row_num, cur_column_num)

        except Person.DoesNotExist:
            pass
        return cur_column_num

    def _write_person_basic_info(self, person_model, excelSheet, row_num, col_num):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.ssn)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.gender)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.birth_date, CompanyUsersSummaryExcelExportView.date_field_format)
            return col_num

        # Skip the columns
        return col_num + 6

    def _write_person_phone_info(self, person_model, phone_type, excelSheet, row_num, col_num):
        phones = person_model.phones.filter(phone_type=phone_type)
        phone_num = None
        if(len(phones) > 0):
            phone_num = phones[0].number
        return self._write_field(excelSheet, row_num, col_num, phone_num)  

    def _write_person_address_info(self, person_model, address_type, excelSheet, row_num, col_num):
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

    def _write_all_family_members_personal_info(self, person_model, excelSheet, row_num, col_num):
        # TODO:
        # BSS only wants spouse and dependent info, maybe we need to better define what relationships
        # are considered "dependent", and white list here instead
        family_members = Person.objects.filter(user=person_model.user).exclude(relationship='self')

        # Write spouse
        spouse_set = family_members.filter(relationship='spouse')
        spouse = None
        if (len(spouse_set) > 0):
            spouse = spouse_set[0]
        col_num = self._write_family_member_personal_info(spouse, excelSheet, row_num, col_num)

        # Write all other family members
        # TODO:
        #   BSS's spreadsheet makes space for 10 dependents. Is there a better way to not be so 
        #   rigid? Or is this actually good enough?
        other_members = family_members.exclude(relationship='spouse')
        members_array = [None] * 10
        for i in range(min(len(other_members), 10)):
            members_array[i] = other_members[i]
        for member in members_array:
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

    def _write_employee_basic_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=employee_user_id).filter(life_insurance__life_insurance_plan__insurance_type='Basic')
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.life_insurance
            plan = company_plan.life_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan.insurance_amount)

            return col_num

        return col_num + 2   

    def _write_employee_optional_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        # TODO:
        # Stub as placeholder 
        return col_num

    def _write_employee_fsa_info(self, employee_user_id, excelSheet, row_num, col_num):
        # TODO:
        # Stub as placeholder 
        return col_num

    def get(self, request, pk, format=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet('All Employee Summary')
        self._write_headers(sheet)
        self._write_company(pk, sheet)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=employee_summary.xls'
        book.save(response)
        return response

