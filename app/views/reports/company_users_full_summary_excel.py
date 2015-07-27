
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

from app.views.permission import (
    user_passes_test,
    company_employer,
    company_employer_or_broker)
from excel_export_view_base import ExcelExportViewBase
from report_export_view_base import ReportExportViewBase

User = get_user_model()

class CompanyUsersFullSummaryExcelExportView(ExcelExportViewBase):

    def _write_headers(self, excelSheet, max_dependents):
        col_num = 0
        col_num = self._write_field(excelSheet, 0, col_num, 'First Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Middle Initial')
        col_num = self._write_field(excelSheet, 0, col_num, 'Last Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'SSN')
        col_num = self._write_field(excelSheet, 0, col_num, 'Gender')
        col_num = self._write_field(excelSheet, 0, col_num, 'Birth Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med PCP NO.')
        col_num = self._write_field(excelSheet, 0, col_num, 'Date of Hire')
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
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Med PCP NO.')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Relationship')

        col_num = self._write_field(excelSheet, 0, col_num, 'Med Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Waived')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Waived Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'Med Last Update Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Waived')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dental Last Update Date')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Option Elected')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Waived')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'Vision Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'STD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'STD Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'LTD Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Total Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life (AD&D) Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'Basic Life Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Total Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Employee Optional Life Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Total Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Spouse Optional Life Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Total Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Child Optional Life Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Total Monthly Premium')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Employee Premium (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'Optional Life Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'FSA Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Dependent FSA Amount')
        col_num = self._write_field(excelSheet, 0, col_num, 'Pay Withhold Amount (Per Pay Period)')
        col_num = self._write_field(excelSheet, 0, col_num, 'FSA Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'FSA Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'FSA Last Update Date')

        col_num = self._write_field(excelSheet, 0, col_num, 'HRA Plan Name')
        col_num = self._write_field(excelSheet, 0, col_num, 'HRA Last Update Reason')
        col_num = self._write_field(excelSheet, 0, col_num, 'HRA Last Update Reason Notes')
        col_num = self._write_field(excelSheet, 0, col_num, 'HRA Last Update Date')

        for i in range(0, max_dependents):
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep First Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Middle Initial ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Last Name ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep SSN ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Gender ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Birth Date ' + `i+1`)
            col_num = self._write_field(excelSheet, 0, col_num, 'Dep Med PCP NO. ' + `i+1`)
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
        start_column_num = self._write_employee_personal_info(employee_user_id, True, True, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_all_health_benefits_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_std_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_ltd_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_basic_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_supplemental_life_insurance_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_fsa_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_employee_hra_info(employee_user_id, excelSheet, row_num, start_column_num)
        start_column_num = self._write_all_dependents_personal_info(employee_user_id, excelSheet, row_num, start_column_num)
        return

    def _write_employee_personal_info(self, employee_user_id, include_spouse_info, write_pcp, excelSheet, row_num, start_column_num):
        cur_column_num = start_column_num
        person = None
        persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(persons) > 0):
            person = persons[0]
        # All helpers are built with capability of skiping proper number of columns when
        # person given is None. This is to ensure other information written after these
        # would be written to the right columns
        cur_column_num = self._write_person_basic_info(person, write_pcp, excelSheet, row_num, cur_column_num, employee_user_id, True)
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

    def _write_person_basic_info(self, person_model, write_pcp, excelSheet, row_num, col_num, employee_user_id=None, write_employee_profile=False):
        if (person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.first_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.middle_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.last_name)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.ssn)
            col_num = self._write_field(excelSheet, row_num, col_num, person_model.gender)
            col_num = self._write_field(excelSheet, row_num, col_num, ReportExportViewBase.get_date_string(person_model.birth_date))
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
                col_num = col_num + 3
        else:
            # Skip the columns
            col_num = col_num + 6

        # Also output the person's medical PCP number info
        # for now, it is decided that the number stick with the person's
        # information section
        if (write_pcp):
            col_num = self._write_person_PCP_number(person_model, excelSheet, row_num, col_num)

        if write_employee_profile:
            col_num = self._write_employee_profile_info(person_model, excelSheet, row_num, col_num)

        return col_num

    def _write_person_PCP_number(self, person_model, excelSheet, row_num, col_num):
        if (person_model):
            enrolleds = Enrolled.objects.filter(user_company_benefit_plan_option__benefit__benefit_plan__benefit_type__name='Medical', person=person_model.id)
            if (len(enrolleds) > 0):
                enrolled = enrolleds[0]
                if (enrolled.pcp):
                    return self._write_field(excelSheet, row_num, col_num, enrolled.pcp)

        return col_num + 1

    def _write_employee_profile_info(self, person_model, excelSheet, row_num, col_num):
        if person_model:
            employee_profiles = EmployeeProfile.objects.filter(person=person_model)
            if len(employee_profiles) > 0 and employee_profiles[0].start_date:
                return self._write_field(excelSheet, row_num, col_num, ReportExportViewBase.get_date_string(employee_profiles[0].start_date))
        return col_num + 1

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
        col_num = self._write_person_basic_info(family_person_model, True, excelSheet, row_num, col_num)

        if (family_person_model):
            col_num = self._write_field(excelSheet, row_num, col_num, family_person_model.relationship)
            return col_num

        # Skip the relationship column
        return col_num + 1

    def _write_employee_all_health_benefits_info(self, employee_user_id, excelSheet, row_num, col_num):
        user_benefit_plan_options = UserCompanyBenefitPlanOption.objects.filter(user=employee_user_id)
        user_benefit_waived = UserCompanyWaivedBenefit.objects.filter(user=employee_user_id)

        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Medical', excelSheet, row_num, col_num)
        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Dental', excelSheet, row_num, col_num)
        col_num = self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, 'Vision', excelSheet, row_num, col_num)

        return col_num

    def _write_employee_health_benefit_info(self, employee_health_benefit_options, employee_health_waived_benefit, benefit_type, excelSheet, row_num, col_num):
        user_benefit_options = employee_health_benefit_options.filter(benefit__benefit_plan__benefit_type__name = benefit_type)
        user_waived_benefit = employee_health_waived_benefit.filter(benefit_type__name = benefit_type)

        if len(user_benefit_options) > 0:
            user_benefit_option = user_benefit_options[0]
            company_plan_option = user_benefit_option.benefit
            benefit_plan = company_plan_option.benefit_plan
            col_num = self._write_field(excelSheet, row_num, col_num, benefit_plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.benefit_option_type)
            if benefit_type == 'Medical':
                col_num = col_num + 2
            else:
                col_num = col_num + 1
            col_num = self._write_field(excelSheet, row_num, col_num, company_plan_option.total_cost_per_period)
            employee_premium = float(company_plan_option.employee_cost_per_period) * company_plan_option.company.pay_period_definition.month_factor
            col_num = self._write_field(excelSheet, row_num, col_num, employee_premium)
            col_num = self._write_employee_benefit_record_reason(user_benefit_option, excelSheet, row_num, col_num)
            return col_num

        elif len(user_waived_benefit) > 0:
            user_waived = user_waived_benefit[0]
            col_num = col_num + 2
            col_num = self._write_field(excelSheet, row_num, col_num, "Waived")
            if benefit_type == 'Medical':
                col_num = self._write_field(excelSheet, row_num, col_num, user_waived.reason)
            col_num = self._write_field(excelSheet, row_num, col_num, "0")
            col_num = self._write_field(excelSheet, row_num, col_num, "0")
            col_num = self._write_employee_benefit_record_reason(user_waived, excelSheet, row_num, col_num)
            return col_num

        if benefit_type == 'Medical':
            return col_num + 9
        else:
            return col_num + 8

    def _write_disability_insurance_premium_info(self, 
                                                 company_plan, 
                                                 annual_max_benefit, 
                                                 employee_profile, 
                                                 excelSheet, 
                                                 row_num, 
                                                 col_num):
        if employee_profile:
            salary = employee_profile.annual_base_salary
            benefit_from_salary = salary * company_plan.percentage_of_salary / 100
            max_benefit_amount = max(annual_max_benefit, benefit_from_salary)
            total_premium = max_benefit_amount / 12 * company_plan.rate / 10
            if not total_premium:
                total_premium = 0
            col_num = self._write_field(excelSheet, row_num, col_num, total_premium)
            employee_contribution_percent = 0
            if company_plan.employer_contribution_percentage:
                employee_contribution_percent = 100 - company_plan.employer_contribution_percentage
            employee_premium = 0
            if employee_contribution_percent and employee_contribution_percent > 0:
                employee_premium = float(total_premium) *  float(employee_contribution_percent) / 100 * company_plan.company.pay_period_definition.month_factor
            if not employee_premium:
                employee_premium = 0
            col_num = self._write_field(excelSheet, row_num, col_num, employee_premium)
        else:
            col_num = self._write_field(excelSheet, row_num, col_num, 'No Employee Salary')
            col_num = self._write_field(excelSheet, row_num, col_num, 'No Employee Salary')
        return col_num

    def _write_employee_std_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyStdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            if employee_plan.company_std_insurance:
                company_plan = employee_plan.company_std_insurance
                plan = company_plan.std_insurance_plan
                col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
                col_num = self._write_field(excelSheet, row_num, col_num, str(company_plan.percentage_of_salary) + '% of Salary')
                employee_profile = self._get_employee_profile_by_user_id(employee_user_id)
                annual_max_benefit = company_plan.max_benefit_weekly * 52;
                col_num = self._write_disability_insurance_premium_info(company_plan, 
                                                                        annual_max_benefit, 
                                                                        employee_profile, 
                                                                        excelSheet, 
                                                                        row_num, 
                                                                        col_num)
                col_num = self._write_employee_benefit_record_reason(employee_plan, excelSheet, row_num, col_num)

                return col_num
            else:
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num += 2
                col_num = self._write_employee_benefit_record_reason(employee_plan, excelSheet, row_num, col_num)

        return col_num + 7

    def _write_employee_ltd_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLtdInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_ltd_insurance
            plan = company_plan.ltd_insurance_plan
            col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
            col_num = self._write_field(excelSheet, row_num, col_num, str(company_plan.percentage_of_salary) + '% of Salary')
            employee_profile = self._get_employee_profile_by_user_id(employee_user_id)
            annual_max_benefit = company_plan.max_benefit_monthly * 12;
            col_num = self._write_disability_insurance_premium_info(company_plan, 
                                                                    annual_max_benefit, 
                                                                    employee_profile, 
                                                                    excelSheet, 
                                                                    row_num, 
                                                                    col_num)
            col_num = self._write_employee_benefit_record_reason(employee_plan, excelSheet, row_num, col_num)

            return col_num

        return col_num + 7

    def _write_employee_basic_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=employee_user_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]

            if (employee_plan.company_life_insurance):
                company_plan = employee_plan.company_life_insurance
                plan = company_plan.life_insurance_plan
                col_num = self._write_field(excelSheet, row_num, col_num, plan.name)
                insurance_total = company_plan.insurance_amount
                if not insurance_total and company_plan.salary_multiplier:
                    employee_profile = self._get_employee_profile_by_user_id(employee_user_id)
                    if employee_profile:
                        insurance_total = employee_profile.annual_base_salary * company_plan.salary_multiplier
                    else:
                        insurance_total = 'No Salary Info'
                col_num = self._write_field(excelSheet, row_num, col_num, insurance_total)
                col_num = self._write_field(excelSheet, row_num, col_num, company_plan.total_cost_per_period)
                employee_premium = float(company_plan.employee_cost_per_period) * company_plan.company.pay_period_definition.month_factor
                col_num = self._write_field(excelSheet, row_num, col_num, employee_premium)
                col_num = self._write_employee_benefit_record_reason(employee_plan, excelSheet, row_num, col_num)
                return col_num
            else:
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num += 2
                col_num = self._write_employee_benefit_record_reason(employee_plan, excelSheet, row_num, col_num)
                return col_num

        return col_num + 7

    def _write_employee_supplemental_life_insurance_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = PersonCompSupplLifeInsurancePlan.objects.filter(person=employee_person.id)
            if (len(employee_plans) > 0):
                plan = employee_plans[0]

                if plan.company_supplemental_life_insurance_plan:
                    # Employee
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.self_elected_amount)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.self_premium_per_month)
                    employee_self_premium = float(plan.self_premium_per_month) * plan.company_supplemental_life_insurance_plan.company.pay_period_definition.month_factor
                    col_num = self._write_field(excelSheet, row_num, col_num, employee_self_premium)
                    # Spouse
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.spouse_elected_amount)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.spouse_premium_per_month)
                    employee_spouse_premium = float(plan.spouse_premium_per_month) * plan.company_supplemental_life_insurance_plan.company.pay_period_definition.month_factor
                    col_num = self._write_field(excelSheet, row_num, col_num, employee_spouse_premium)
                    # Child
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.child_elected_amount)
                    col_num = self._write_field(excelSheet, row_num, col_num, plan.child_premium_per_month)
                    employee_child_premium = float(plan.child_premium_per_month) * plan.company_supplemental_life_insurance_plan.company.pay_period_definition.month_factor
                    col_num = self._write_field(excelSheet, row_num, col_num, employee_child_premium)
                    total_premium = plan.self_premium_per_month + plan.spouse_premium_per_month + plan.child_premium_per_month
                    col_num = self._write_field(excelSheet, row_num, col_num, total_premium)
                    total_employee_premium = employee_self_premium + employee_spouse_premium + employee_child_premium
                    col_num = self._write_field(excelSheet, row_num, col_num, total_employee_premium)
                    col_num = self._write_employee_benefit_record_reason(plan, excelSheet, row_num, col_num)
                    return col_num
                else:
                    for i in range(14):
                        col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                    col_num = self._write_employee_benefit_record_reason(plan, excelSheet, row_num, col_num)
                    return col_num
        return col_num + 17

    def _write_employee_fsa_info(self, employee_user_id, excelSheet, row_num, col_num):
        fsas = FSA.objects.filter(user=employee_user_id)
        if (len(fsas) > 0):
            fsa = fsas[0]
            if (fsa.company_fsa_plan):
                col_num = self._write_field(excelSheet, row_num, col_num, fsa.primary_amount_per_year)
                col_num = self._write_field(excelSheet, row_num, col_num, fsa.dependent_amount_per_year)
                fsa_employee_withhold = float((fsa.primary_amount_per_year + fsa.dependent_amount_per_year)) / 12 * fsa.company_fsa_plan.company.pay_period_definition.month_factor
                col_num = self._write_field(excelSheet, row_num, col_num, fsa_employee_withhold) 
                col_num = self._write_employee_benefit_record_reason(fsa, excelSheet, row_num, col_num)
                return col_num
            else:
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num = self._write_field(excelSheet, row_num, col_num, 'Waived')
                col_num = self._write_employee_benefit_record_reason(fsa, excelSheet, row_num, col_num)
                return col_num

        return col_num + 6

    def _write_employee_hra_info(self, employee_user_id, excelSheet, row_num, col_num):
        employee_persons = Person.objects.filter(user=employee_user_id, relationship='self')
        if (len(employee_persons) > 0):
            employee_person = employee_persons[0]
            employee_plans = PersonCompanyHraPlan.objects.filter(person=employee_person.id)
            if (len(employee_plans) > 0):
                plan = employee_plans[0]
                col_num = self._write_field(excelSheet, row_num, col_num, plan.company_hra_plan.hra_plan.name)
                col_num = self._write_employee_benefit_record_reason(plan, excelSheet, row_num, col_num)
                return col_num
        return col_num + 4

    def _write_employee_benefit_record_reason(self, employee_benefit_record, excelSheet, row_num, col_num):
        if (employee_benefit_record.record_reason):
            col_num = self._write_field(excelSheet, row_num, col_num, employee_benefit_record.record_reason.name)
        else:
            col_num = col_num + 1

        col_num = self._write_field(excelSheet, row_num, col_num, employee_benefit_record.record_reason_note)
        col_num = self._write_field(excelSheet, row_num, col_num, ReportExportViewBase.get_date_string(employee_benefit_record.updated_at))

        return col_num

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
