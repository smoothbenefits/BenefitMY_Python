import time
from StringIO import StringIO

from django.http import HttpResponse
from django.contrib.auth import get_user_model

from report_service_base import ReportServiceBase
from pdf_report_service_base import PdfReportServiceBase

from app.models.company import Company
from app.models.person import Person
from app.models.company_group_member import CompanyGroupMember
from app.models.health_benefits.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption
from app.models.health_benefits.company_group_benefit_plan_option import CompanyGroupBenefitPlanOption
from app.models.health_benefits.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.company_group_basic_life_insurance_plan import CompanyGroupBasicLifeInsurancePlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import PersonCompSupplLifeInsurancePlan
from app.models.insurance.company_group_suppl_life_insurance_plan import CompanyGroupSupplLifeInsurancePlan
from app.models.insurance.std_insurance_plan import StdInsurancePlan
from app.models.insurance.company_group_std_insurance_plan import CompanyGroupStdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan
from app.models.insurance.company_group_ltd_insurance_plan import CompanyGroupLtdInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.hra.company_group_hra_plan import CompanyGroupHraPlan
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.fsa.fsa import FSA
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from app.models.hsa.company_group_hsa_plan import CompanyGroupHsaPlan
from app.models.hsa.person_company_group_hsa_plan import PersonCompanyGroupHsaPlan
from app.models.commuter.company_commuter_plan import CompanyCommuterPlan
from app.models.commuter.person_company_commuter_plan import PersonCompanyCommuterPlan
from app.models.document import Document

from app.service.disability_insurance_service import DisabilityInsuranceService
from app.service.life_insurance_service import LifeInsuranceService

User = get_user_model()


class CompanyEmployeeBenefitPdfReportService(PdfReportServiceBase):

    def get_all_employees_resport(self, company_id, outputStream):
        # initialize the canvas
        self._init_canvas(outputStream)
        self._write_company(company_id)
        self._save()

    def get_employee_report(self, employee_user_id, company_id, outputStream):
        self._init_canvas(outputStream)
        self._write_employee(employee_user_id, company_id)
        self._save()

    def _write_company(self, company_id):
        users_id = self._get_all_employee_user_ids_for_company(company_id)

        # For each of them, write out his/her information
        for i in range(len(users_id)):
            self._write_employee(users_id[i], company_id)

        return

    def _get_page_title(self, company_id):
        comp = Company.objects.get(pk=company_id)
        if comp:
            return comp.name + ' - Enrollment Confirmation - ' + \
                time.strftime('%B') + ' ' + time.strftime('%Y')
        else:
            return ''

    def _get_user_company_group(self, user_id):
        comp_group_members = CompanyGroupMember.objects.filter(user=user_id)
        if comp_group_members:
            return comp_group_members[0].company_group.id
        else:
            return None

    def _write_employee(self, employee_user_id, company_id):
        person = self._get_person_by_user(employee_user_id)
        user = self._get_user_by_id(employee_user_id)
        company_group_id = self._get_user_company_group(employee_user_id)

        # set the common configuration on the page
        self._init_page()

        # Write title of the page
        title = self._get_page_title(company_id)
        self._set_font(14)
        self._write_line([title])
        self._start_new_line()

        # Write full name of the employee being rendered
        self._set_font(12)
        full_name = self._get_person_full_name(person, user)
        self._write_line([full_name])

        self._start_new_line()
        self._set_font(10)

        # Write employee type and address
        self._write_employee_meta_info(person)

        # Now starts writing benefit enrollments
        self._write_employee_all_health_benefits_info(user, company_group_id)
        self._write_employee_basic_life_insurance_info(user, person, company_group_id)
        self._write_employee_hra_info(person, company_group_id)
        self._write_employee_supplemental_life_insurance_info(person, company_group_id)
        self._write_employee_std_insurance_info(user, company_group_id)
        self._write_employee_ltd_insurance_info(user, company_group_id)
        self._write_employee_hsa_info(person, company_group_id)
        self._write_employee_fsa_info(user, company_id)
        self._write_employee_commuter_info(person, company_id)

        # extra space between main sections
        self._start_new_line()
        self._start_new_line()

        # Now move onto documents
        self._write_employee_all_documents_info(user)

        # end the current page for the current employ
        # and start a new one for the next
        self._start_new_page()

        return

    def _write_employee_meta_info(self, person):
        # Write employment type
        employee_profile = self._get_employee_profile_by_person(person)
        employee_address = self._get_address_by_person(person)
        meta_info = []
        width_array = []
        if employee_profile:
            meta_info.append(employee_profile.employment_type)
            width_array.append(0.5)

        if employee_address:
            meta_info.append("{} {}, {} {} {}".format(employee_address.street_1, employee_address.street_2, employee_address.city, employee_address.state, employee_address.zipcode))
            width_array.append(0.5)

        if meta_info:
            self._write_line_uniform_width(meta_info, width_array)
            self._start_new_line()

    def _write_not_selected_plan(self, benefit_name):
        # Render header
        self._write_line_uniform_width([benefit_name])
        self._draw_line()
        self._write_line_uniform_width(['Not Selected'])
        self._start_new_line()
        self._start_new_line()

    def _write_waived_plan(self, benefit_name):
        # Render header
        self._write_line_uniform_width([benefit_name])
        self._draw_line()
        self._write_line_uniform_width(['Waived'])
        self._start_new_line()
        self._start_new_line()

    def _get_beneficiary_tier(self, tier_number):
        if tier_number == '1':
            return 'Primary'
        else:
            return 'Contingent'

    def _write_beneficiaries(self, plan_name, beneficiaries):
        if not beneficiaries:
            return

        self._write_line_uniform_width([' ', '{} Beneficiaries:'.format(plan_name)], [0.1, 0.9])
        self._start_new_line()
        column_width_dists = [0.1, 0.1, 0.1, 0.1, 0.15, 0.2, 0.15, 0.1]
        self._write_line_uniform_width([' ', 'Tier', 'First Name', 'Last Name', 'Relationship', 'Email', 'Phone', 'Percentage'], column_width_dists)
        self._draw_line(56)
        for beneficiary in beneficiaries:
            self._write_line_uniform_width([' ', '{}'.format(self._get_beneficiary_tier(beneficiary.tier)), beneficiary.first_name, beneficiary.last_name, beneficiary.relationship, beneficiary.email, beneficiary.phone, beneficiary.percentage],
                                               column_width_dists)

        self._start_new_line()
        self._start_new_line()

    def _write_employee_all_health_benefits_info(self, user_model, company_group_id):
        user_benefit_plan_options = UserCompanyBenefitPlanOption.objects.filter(user=user_model.id)
        user_benefit_waived = UserCompanyWaivedBenefit.objects.filter(user=user_model.id)
        company_benefit_list = CompanyGroupBenefitPlanOption.objects.filter(company_group=company_group_id)

        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Medical')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Dental')
        self._write_employee_health_benefit_info(user_benefit_plan_options, user_benefit_waived, company_benefit_list, 'Vision')

        return

    def _write_employee_health_benefit_info(self, employee_health_benefit_options, employee_health_waived_benefit, company_benefit_list, benefit_type):
        user_benefit_options = employee_health_benefit_options.filter(benefit__benefit_plan__benefit_type__name = benefit_type)
        user_waived_benefit = employee_health_waived_benefit.filter(benefit_type__name = benefit_type)
        company_plan_options = company_benefit_list.filter(company_benefit_plan_option__benefit_plan__benefit_type__name = benefit_type)

        if len(user_benefit_options) > 0:
            # column width distributions
            column_width_dists = [0.45, 0.35, 0.2]

            # Render header
            self._write_line_uniform_width(
                [benefit_type + ' Plan', 'Enrolled Members', 'Employee Premium'],
                column_width_dists)
            self._draw_line()

            user_benefit_option = user_benefit_options[0]
            company_plan_option = user_benefit_option.benefit
            benefit_plan = company_plan_option.benefit_plan

            # Get enrolled members
            enrolled_members = user_benefit_option.enrolleds

            text_block = [[], [], []]
            text_block[0].append(benefit_plan.name)
            text_block[0].append(company_plan_option.benefit_option_type)
            pay_period_month_factor = company_plan_option.company.pay_period_definition.month_factor
            text_block[2].append("${:.2f}".format(float(company_plan_option.employee_cost_per_period) * pay_period_month_factor))
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

            self._write_line_uniform_width([
                'Waived',
                user_waived.reason])
            self._start_new_line()
            self._start_new_line()

        elif len(company_plan_options) > 0:
            self._write_not_selected_plan(benefit_type + ' Plan')

        return

    def _write_employee_basic_life_insurance_info(self, user_model, person_model, company_group_id):
        employee_plans = UserCompanyLifeInsurancePlan.objects.filter(user=user_model.id)
        company_plans = CompanyGroupBasicLifeInsurancePlan.objects.filter(company_group=company_group_id)

        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]

            if (employee_plan.company_life_insurance):
                # Render header
                column_width_dists = [0.45, 0.35, 0.2]
                self._write_line_uniform_width(['Basic Life (AD&D)', 'Coverage', 'Employee Premium'],
                                               column_width_dists)
                self._draw_line()

                company_plan = employee_plan.company_life_insurance
                plan = company_plan.life_insurance_plan
                life_insurance_service = LifeInsuranceService(company_plan)
                cost = life_insurance_service.get_basic_life_insurance_cost_for_employee(person_model.id)

                # Convert employee premium to per pay period from per month
                month_factor = employee_plan.company_life_insurance.company.pay_period_definition.month_factor
                employee_premium = "${:.2f}".format(float(cost.employee_cost) * month_factor)
                self._write_line_uniform_width([plan.name, cost.benefit_amount, employee_premium],
                                               column_width_dists)
                self._start_new_line()
                self._start_new_line()
                beneficiaries = employee_plan.life_insurance_beneficiary.all().order_by('tier')
                self._write_beneficiaries('Basic Life (AD&D)', beneficiaries)
            else:
                self._write_waived_plan('Basic Life (AD&D)')

        elif company_plans:
            self._write_not_selected_plan('Basic Life (AD&D)')

        return

    def _write_employee_hra_info(self, person_model, company_group_id):
        company_plans = CompanyGroupHraPlan.objects.filter(company_group=company_group_id)
        plan_selected = False
        if (person_model):
            employee_plans = PersonCompanyHraPlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan_selected = True
                plan = employee_plans[0]
                if plan.company_hra_plan:
                    # Render header
                    self._write_line_uniform_width(['HRA Plan', 'Description'])
                    self._draw_line()
                    self._write_line_uniform_width([
                        plan.company_hra_plan.hra_plan.name,
                        plan.company_hra_plan.hra_plan.description])

                    self._start_new_line()
                    self._start_new_line()
                else:
                    self._write_waived_plan('HRA Plan')

        if not plan_selected and company_plans:
            self._write_not_selected_plan('HRA Plan')

        return

    def _write_employee_supplemental_life_insurance_info(self, person_model, company_group_id):
        plan_selected = False
        company_plans = CompanyGroupSupplLifeInsurancePlan.objects.filter(company_group=company_group_id)
        if (person_model):
            employee_plans = PersonCompSupplLifeInsurancePlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan_selected = True
                plan = employee_plans[0]

                if plan.company_supplemental_life_insurance_plan:
                    # Render header
                    self._write_line_uniform_width(['Suppl. Life Plan', 'Coverage Target', 'Elected Amount', 'Premium', 'Condition'])
                    self._draw_line()

                    text_block = [[],[],[],[],[]]
                    text_block[0].append(plan.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name)

                    text_block[1].append('Employee')
                    text_block[1].append('Spouse')
                    text_block[1].append('Child(ren)')

                    text_block[2].append(plan.self_elected_amount)
                    text_block[2].append(plan.spouse_elected_amount)
                    text_block[2].append(plan.child_elected_amount)
                    month_factor = plan.company_supplemental_life_insurance_plan.company.pay_period_definition.month_factor
                    text_block[3].append("${:.2f}".format(float(plan.self_premium_per_month) * month_factor))
                    text_block[3].append("${:.2f}".format(float(plan.spouse_premium_per_month) * month_factor))
                    text_block[3].append("${:.2f}".format(float(plan.child_premium_per_month) * month_factor))

                    text_block[4].append(plan.self_condition.name)
                    text_block[4].append(plan.spouse_condition.name)
                    text_block[4].append('N/A')

                    self._write_block_uniform_width(text_block)

                    self._start_new_line()
                    self._start_new_line()

                    beneficiaries = plan.suppl_life_insurance_beneficiary.all().order_by('tier')
                    self._write_beneficiaries('Suppl. Life Plan', beneficiaries)
                else:
                    self._write_waived_plan('Supplemental Life Plan')

        if not plan_selected and company_plans:
            self._write_not_selected_plan('Suppl. Life Plan')

        return

    def _write_employee_std_insurance_info(self, user_model, company_group_id):
        employee_plans = UserCompanyStdInsurancePlan.objects.filter(user=user_model.id)
        company_plans = CompanyGroupStdInsurancePlan.objects.filter(company_group=company_group_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]

            if employee_plan.company_std_insurance:
                # Render header
                self._write_line_uniform_width(['STD Plan', 'Employee Premium'])
                self._draw_line()

                company_plan = employee_plan.company_std_insurance
                plan = company_plan.std_insurance_plan
                # get the premium
                disability_service = DisabilityInsuranceService(company_plan)
                employee_premium = disability_service.get_employee_premium(employee_plan.total_premium_per_month)
                self._write_line_uniform_width([plan.name, "${:.2f}".format(employee_premium)])
                self._start_new_line()
                self._start_new_line()
            else:
                self._write_waived_plan('STD Plan')
        elif company_plans:
            self._write_not_selected_plan('STD Plan')

        return

    def _write_employee_ltd_insurance_info(self, user_model, company_group_id):
        employee_plans = UserCompanyLtdInsurancePlan.objects.filter(user=user_model.id)
        company_plans = CompanyGroupLtdInsurancePlan.objects.filter(company_group=company_group_id)
        if (len(employee_plans) > 0):
            employee_plan = employee_plans[0]
            if employee_plan.company_ltd_insurance:
                # Render header
                self._write_line_uniform_width(['LTD Plan', 'Employee Premium'])
                self._draw_line()
                company_plan = employee_plan.company_ltd_insurance

                # get the premium
                disability_service = DisabilityInsuranceService(company_plan)
                employee_premium = disability_service.get_employee_premium(employee_plan.total_premium_per_month)
                plan = company_plan.ltd_insurance_plan
                self._write_line_uniform_width([plan.name, "${:.2f}".format(employee_premium)])
                self._start_new_line()
                self._start_new_line()
            else:
                self._write_waived_plan('LTD Plan')
        elif company_plans:
            self._write_not_selected_plan('LTD Plan')

        return

    def _write_employee_fsa_info(self, user_model, company_id):
        fsas = FSA.objects.filter(user=user_model.id)
        company_plans = CompanyFsaPlan.objects.filter(company=company_id)
        if (len(fsas) > 0):
            fsa = fsas[0]
            if (fsa.company_fsa_plan):
                # Render header
                self._write_line_uniform_width(['Account Type', 'Elected Annual Amount', 'Paycheck Withhold'])
                self._draw_line()

                month_factor = fsa.company_fsa_plan.company.pay_period_definition.month_factor
                self._write_line_uniform_width(['Health Account', fsa.primary_amount_per_year, "${:.2f}".format(float(fsa.primary_amount_per_year) / 12 * month_factor)])
                self._write_line_uniform_width(['Dependent Care Account', fsa.dependent_amount_per_year, "${:.2f}".format(float(fsa.dependent_amount_per_year) / 12 * month_factor)])

                self._start_new_line()
                self._start_new_line()
            else:
                self._write_waived_plan('Flexible Spending Account')
        elif company_plans:
            self._write_not_selected_plan('Flexible Spending Account')

        return

    def _write_employee_hsa_info(self, person_model, company_group_id):
        plan_selected = False
        group_plans = CompanyGroupHsaPlan.objects.filter(company_group=company_group_id)
        if (person_model):
            employee_plans = PersonCompanyGroupHsaPlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan = employee_plans[0]
                plan_selected = True
                if (plan.company_hsa_plan):
                    # Render header
                    self._write_line_uniform_width(['HSA Plan', 'Selected Amount Per Year'])
                    self._draw_line()

                    self._write_line_uniform_width([
                        plan.company_hsa_plan.name,
                        self._normalize_dollar_amount(plan.amount_per_year)])

                    self._start_new_line()
                    self._start_new_line()
                else:
                    self._write_waived_plan('Health Savings Account')
        if not plan_selected and group_plans:
            self._write_not_selected_plan('Health Savings Account')

        return

    def _write_employee_commuter_info(self, person_model, company_id):
        company_plans = CompanyCommuterPlan.objects.filter(company=company_id)
        plan_selected = False
        if (person_model):
            employee_plans = PersonCompanyCommuterPlan.objects.filter(person=person_model.id)
            if (len(employee_plans) > 0):
                plan_selected = True
                # Render header
                # Split onto
                self._write_line_uniform_width(['Commuter Plan', 'Transit/Month', 'Transit/Month', 'Parking/Month', 'Parking/Month'])
                self._write_line_uniform_width(['', '(Pre-Tax)', '(Post-Tax)', '(Pre-Tax)', '(Post-Tax)'])
                self._draw_line()

                plan = employee_plans[0]
                self._write_line_uniform_width([
                    plan.company_commuter_plan.plan_name,
                    self._normalize_dollar_amount(plan.monthly_amount_transit_pre_tax),
                    self._normalize_dollar_amount(plan.monthly_amount_transit_post_tax),
                    self._normalize_dollar_amount(plan.monthly_amount_parking_pre_tax),
                    self._normalize_dollar_amount(plan.monthly_amount_parking_post_tax)])

                self._start_new_line()
                self._start_new_line()

        if not plan_selected and company_plans:
            self._write_not_selected_plan('Commuter Plan')

        return

    def _write_employee_all_documents_info(self, user_model):
        documents = Document.objects.filter(user=user_model.id)
        if (len(documents) > 0):
            self._write_line(['Documents:'])
            self._draw_line()

            for document in documents:
                self._write_line_uniform_width([
                    document.name,
                    'Signed' if document.signature is not None else 'Not Signed',
                    ReportServiceBase.get_date_string(document.signature.created_at) if document.signature is not None else ''
                ],
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

    def _get_employee_profile_by_person(self, person_model):
        if (person_model):
            profiles = person_model.employee_profile_person.all()
            if (len(profiles) > 0):
                return profiles[0]
        return None

    def _get_address_by_person(self, person_model):
        if person_model:
            addresses = person_model.addresses.all()
            for ads in addresses:
                if ads.address_type == 'home':
                    return ads
            if len(addresses) > 0:
                return addresses[0]
        return None


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
