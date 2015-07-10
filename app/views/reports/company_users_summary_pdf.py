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
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from app.models.sys_benefit_update_reason import SysBenefitUpdateReason
from app.models.document import Document
from app.models.document_type import DocumentType
from app.models.signature import Signature
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
            self._write_employee(users_id[i], company_id)

        return

    def _get_person_birth_date_line(self, person):
        if person and person.birth_date:
            return '(' + person.birth_date.strftime("%Y-%m-%d") + ')'
        else:
            return ''

    def _write_employee(self, employee_user_id, company_id):
        person = self._get_person_by_user(employee_user_id)
        user = self._get_user_by_id(employee_user_id)

        # set the common configuration on the page
        self._init_page()

        # Write full name of the employee being rendered
        full_name = self._get_person_full_name(person, user)
        self._write_line([ \
            full_name, \
            self._get_person_birth_date_line(person) if person is not None else ''])

        self._start_new_line()

        # Now starts writing benefit enrollments
        self._write_employee_all_health_benefits_info(user, company_id)
        self._write_employee_basic_life_insurance_info(user, person, company_id)
        self._write_employee_hra_info(person, company_id)
        self._write_employee_supplemental_life_insurance_info(person, company_id)
        self._write_employee_std_insurance_info(user, company_id)
        self._write_employee_ltd_insurance_info(user, company_id)
        self._write_employee_fsa_info(user, company_id)

        # extra space between main sections
        self._start_new_line()
        self._start_new_line()

        # Now move onto documents
        self._write_employee_all_documents_info(user)

        # end the current page for the current employ
        # and start a new one for the next
        self._start_new_page()

        return

    def _write_not_selected_plan(self, benefit_name):
        # Render header
        self._write_line_uniform_width([benefit_name])
        self._draw_line()
        self._write_line_uniform_width(['Not Selected'])
        self._start_new_line()
        self._start_new_line()

    def _write_employee_all_health_benefits_info(self, user_model, company_id):
        user_benefit_plan_options = UserCompanyBenefitPlanOption.objects.filter(user=user_model.id)
        user_benefit_waived = UserCompanyWaivedBenefit.objects.filter(user=user_model.id)
        company_benefit_list = CompanyBenefitPlanOption.objects.filter(company=company_id)

        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Medical')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Dental')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Vision')

        return

    def _write_employee_health_benefit_info(self, employee_health_benefit_options, employee_health_waived_benefit, company_benefit_list, benefit_type):
        user_benefit_options = employee_health_benefit_options.filter(benefit__benefit_plan__benefit_type__name = benefit_type)
        user_waived_benefit = employee_health_waived_benefit.filter(benefit_type__name = benefit_type)
        company_plan_options = company_benefit_list.filter(benefit_plan__benefit_type__name = benefit_type)

        if len(user_benefit_options) > 0:
            # column width distributions
            column_width_dists = [0.45, 0.35, 0.2]

            # Render header
            self._write_line_uniform_width( \
                [benefit_type + ' Plan', 'Enrolled Members', 'Employee Premium'], \
                column_width_dists)
            self._draw_line()

            user_benefit_option = user_benefit_options[0]
            company_plan_option = user_benefit_option.benefit
            benefit_plan = company_plan_option.benefit_plan

            # Get enrolled members
            enrolled_members = user_benefit_option.enrolleds

            text_block = [[],[],[]]
            text_block[0].append(benefit_plan.name)
            text_block[0].append(company_plan_option.benefit_option_type)
            text_block[2].append(company_plan_option.employee_cost_per_period)
            for enrolled_member in enrolled_members.all():
                member_name = self._get_person_full_name(enrolled_member.person)
                relationship = enrolled_member.person.relationship
                text_block[1].append(relationship + ': ' + member_name)

            self._write_block_uniform_width(text_block, column_width_dists)
            self._start_new_line()
            self._start_new_line()

        elif len(user_waived_benefit) > 0:
            # Render header
            self._write_line_uniform_width([benefit_type + ' Plan', 'Waive Reason'])
            self._draw_line()

            user_waived = user_waived_benefit[0]

            self._write_line_uniform_width([ \
                'Waived', \
                user_waived.reason])
            self._start_new_line()
            self._start_new_line()

        elif len(company_plan_options) > 0:
            self._write_not_selected_plan(benefit_type + ' Plan')

        return

    def _write_employee_basic_life_insurance_info(self, user_model, person_model, company_id):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=user_model.id).filter(company_life_insurance__life_insurance_plan__insurance_type='Basic')
        company_plans = CompanyLifeInsurancePlan.objects.filter(company=company_id)

        if (len(employee_plans) > 0):
            # Render header
            column_width_dists = [0.45, 0.35, 0.2]
            self._write_line_uniform_width(['Basic Life (AD&D)', 'Coverage', 'Employee Premium'],
                                           column_width_dists)
            self._draw_line()

            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_life_insurance
            plan = company_plan.life_insurance_plan

            # compute the coverage
            coverage_amount = ''
            if (company_plan.insurance_amount): 
                coverage_amount = company_plan.insurance_amount
            elif (company_plan.salary_multiplier):
                salary = self._get_salary_by_person(person_model)
                if (salary):
                    coverage_amount = company_plan.salary_multiplier * salary
            self._write_line_uniform_width([plan.name, coverage_amount, 'N/A'],
                                           column_width_dists)
            self._start_new_line()
            self._start_new_line()

        elif company_plans:
            self._write_not_selected_plan('Basic Life (AD&D)')

        return

    def _write_employee_hra_info(self, person_model, company_id):
        company_plans = CompanyHraPlan.objects.filter(company=company_id)
        plan_selected = False
        if (person_model):
            employee_plans = PersonCompanyHraPlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan_selected = True
                # Render header
                self._write_line_uniform_width(['HRA Plan', 'Description'])
                self._draw_line()

                plan = employee_plans[0]
                self._write_line_uniform_width([ \
                    plan.company_hra_plan.hra_plan.name, 
                    plan.company_hra_plan.hra_plan.description])
        
                self._start_new_line()
                self._start_new_line()

        if not plan_selected and company_plans:
            self._write_not_selected_plan('HRA Plan')

        return

    def _write_employee_supplemental_life_insurance_info(self, person_model, company_id):
        plan_selected = False
        company_plans = CompSupplLifeInsurancePlan.objects.filter(company=company_id)
        if (person_model):
            employee_plans = PersonCompSupplLifeInsurancePlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan_selected = True
                # Render header
                self._write_line_uniform_width(['Suppl. Life Plan', 'Coverage Target', 'Elected Amount', 'Premium', 'Condition'])
                self._draw_line()

                plan = employee_plans[0]

                text_block = [[],[],[],[],[]]
                text_block[0].append(plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)

                text_block[1].append('Employee')
                text_block[1].append('Spouse')
                text_block[1].append('Child(ren)')

                text_block[2].append(plan.self_elected_amount)
                text_block[2].append(plan.spouse_elected_amount)
                text_block[2].append(plan.child_elected_amount)

                text_block[3].append(plan.self_premium_per_month)
                text_block[3].append(plan.spouse_premium_per_month)
                text_block[3].append(plan.child_premium_per_month)
                
                text_block[4].append(plan.self_condition.name)
                text_block[4].append(plan.spouse_condition.name)
                text_block[4].append('N/A')

                self._write_block_uniform_width(text_block)

                self._start_new_line()
                self._start_new_line()

        if not plan_selected and company_plans:
            self._write_not_selected_plan('Suppl. Life Plan')

        return

    def _write_employee_std_insurance_info(self, user_model, company_id):
        employee_plans = UserCompanyStdInsurancePlan.objects.filter(user=user_model.id)
        company_plans = CompanyStdInsurancePlan.objects.filter(company=company_id)
        if (len(employee_plans) > 0):
            # Render header
            self._write_line_uniform_width(['STD Plan', 'Employee Premium'])
            self._draw_line()

            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_std_insurance
            plan = company_plan.std_insurance_plan

            self._write_line_uniform_width([plan.name, 'N/A'])

            self._start_new_line()
            self._start_new_line()
        elif company_plans:
            self._write_not_selected_plan('STD Plan')

        return

    def _write_employee_ltd_insurance_info(self, user_model, company_id):
        employee_plans = UserCompanyLtdInsurancePlan.objects.filter(user=user_model.id)
        company_plans = CompanyLtdInsurancePlan.objects.filter(company=company_id)
        if (len(employee_plans) > 0):
            # Render header
            self._write_line_uniform_width(['LTD Plan', 'Employee Premium'])
            self._draw_line()

            employee_plan = employee_plans[0]
            company_plan = employee_plan.company_ltd_insurance
            plan = company_plan.ltd_insurance_plan

            self._write_line_uniform_width([plan.name, 'N/A'])

            self._start_new_line()
            self._start_new_line()
        elif company_plans:
            self._write_not_selected_plan('LTD Plan')

        return

    def _write_employee_fsa_info(self, user_model, company_id):
        fsas = FSA.objects.filter(user=user_model.id)
        company_plans = CompanyFsaPlan.objects.filter(company=company_id)
        if (len(fsas) > 0):
            # Render header
            self._write_line_uniform_width(['Account Type', 'Elected Annual Amount'])
            self._draw_line()

            fsa = fsas[0]

            self._write_line_uniform_width(['Health Account', fsa.primary_amount_per_year])
            self._write_line_uniform_width(['Dependent Care Account', fsa.dependent_amount_per_year])
            
            self._start_new_line()
            self._start_new_line()
        elif company_plans:
            self._write_not_selected_plan('Flexible Spending Account')

        return

    def _write_employee_all_documents_info(self, user_model):
        documents = Document.objects.filter(user=user_model.id)
        if (len(documents) > 0):
            self._write_line(['Documents:'])
            self._draw_line()

            for document in documents:
                self._write_line_uniform_width([ \
                    document.name, \
                    'Signed' if document.signature is not None else 'Not Signed', \
                    document.signature.created_at.strftime("%Y-%m-%d") if document.signature is not None else ''
                ], \
                [0.6, 0.2, 0.2])  

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

    def _get_salary_by_person(self, person_model):
        result = None
        if (person_model):
            profiles = person_model.employee_profile_person.all()
            if (len(profiles) > 0):
                profile = profiles[0]
                result = profile.annual_base_salary

        return result

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

