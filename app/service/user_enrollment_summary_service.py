from django.utils import timezone
from app.models.person import Person
from app.models.health_benefits.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.models.health_benefits.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.fsa.fsa import FSA
from app.models.hsa.person_company_group_hsa_plan import PersonCompanyGroupHsaPlan
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan
from app.models.company_group_member import CompanyGroupMember

from app.models.health_benefits.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from app.models.fsa.company_group_fsa_plan import CompanyGroupFsaPlan
from app.models.hsa.company_group_hsa_plan import CompanyGroupHsaPlan
from app.models.hra.company_hra_plan import CompanyHraPlan
from app.models.hra.company_group_hra_plan import CompanyGroupHraPlan
from app.models.insurance.company_life_insurance_plan import CompanyLifeInsurancePlan
from app.models.insurance.company_ltd_insurance_plan import CompanyLtdInsurancePlan
from app.models.insurance.company_std_insurance_plan import CompanyStdInsurancePlan
from app.models.insurance.comp_suppl_life_insurance_plan import CompSupplLifeInsurancePlan

NOT_STARTED = 'NOT_STARTED'
IN_PROGRESS = 'IN_PROGRESS'
COMPLETED = 'COMPLETED'
NO_BENEFITS = 'NO_BENEFITS_OFFERED'

class UserEnrollmentSummaryService(object):
    def __init__(self, company_id, user_id, person_id):
        self.user_id = user_id
        self.person_id = person_id
        self.company_id = company_id

        # Get the user's company group info
        self.company_group = None
        company_group_members = CompanyGroupMember.objects.filter(user=self.user_id)
        if (len(company_group_members) > 0):
            self.company_group = company_group_members[0].company_group

    def get_health_benefit_enrollment(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.health_benefit_plan_option.all()
        if (group_plans.exists()):
            return UserCompanyBenefitPlanOption.objects.filter(user=self.user_id)
        else:
            return None

    def get_health_benefit_waive(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.health_benefit_plan_option.all()
        if (group_plans.exists()):
            return UserCompanyWaivedBenefit.objects.filter(user=self.user_id)
        else:
            return None

    def get_hra_plan(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.hra_plan.all()
        if(group_plans.exists()):
            return PersonCompanyHraPlan.objects.filter(person=self.person_id)
        else:
            return None

    def get_fsa_plan(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.fsa_plan.all()
        if (group_plans.exists()):
            return FSA.objects.filter(user=self.user_id)
        else:
            return None

    def get_basic_life_insurance(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.basic_life_insurance_plan.all()
        if (group_plans.exists()):
            return UserCompanyLifeInsurancePlan.objects.filter(user=self.user_id)
        else:
            return None

    def get_supplimental_life_insurance(self):
        if (not self.company_group):
            return None

        group_plans = self.company_group.suppl_life_insurance_plan.all()
        if(group_plans.exists()):
            return PersonCompSupplLifeInsurancePlan.objects.filter(person=self.person_id)
        else:
            return None

    def get_std_insurance(self):
        if not self.company_group:
            return None
        group_plans = self.company_group.company_std_insurance_plan.all()
        if group_plans.exists():
            return UserCompanyStdInsurancePlan.objects.filter(user=self.user_id)
        else:
            return None

    def get_ltd_insurance(self):
        if not self.company_group:
            return None
        group_plans = self.company_group.company_ltd_insurance_plan.all()
        if group_plans.exists():
            return UserCompanyLtdInsurancePlan.objects.filter(user=self.user_id)
        else:
            return None

    def get_hsa_plan(self):
        if not self.company_group:
            return None

        group_plans = self.company_group.company_hsa_plan.all()
        if (group_plans.exists()):
            return PersonCompanyGroupHsaPlan.objects.filter(person=self.person_id)
        else:
            return None

    def get_enrollment_status(self):
        health_enrollment = self.get_health_benefit_enrollment()
        health_waived = self.get_health_benefit_waive()
        hra_enrollment = self.get_hra_plan()
        fsa_enrollment = self.get_fsa_plan()
        hsa_enrollment = self.get_hsa_plan()
        basic_life_enrollment = self.get_basic_life_insurance()
        ltd_enrollment = self.get_ltd_insurance()
        std_enrollment = self.get_std_insurance()
        suppl_life_enrollment = self.get_supplimental_life_insurance()
        status = IN_PROGRESS
        if health_enrollment == None and \
           health_waived == None and \
           hra_enrollment == None and \
           fsa_enrollment == None and \
           hsa_enrollment == None and \
           basic_life_enrollment == None and \
           suppl_life_enrollment == None and \
           ltd_enrollment == None and \
           std_enrollment == None:
            status = NO_BENEFITS
        elif not health_enrollment and \
           not health_waived and \
           not hra_enrollment and \
           not fsa_enrollment and \
           not hsa_enrollment and \
           not basic_life_enrollment and \
           not suppl_life_enrollment and \
           not ltd_enrollment and \
           not std_enrollment:
            status = NOT_STARTED
        elif ((health_enrollment is None or len(health_enrollment) > 0) or \
             (health_waived is None or len(health_waived) > 0)) and \
             (hra_enrollment is None or len(hra_enrollment) > 0) and \
             (fsa_enrollment is None or len(fsa_enrollment) > 0) and \
             (hsa_enrollment is None or len(hsa_enrollment) > 0) and \
             (basic_life_enrollment is None or len(basic_life_enrollment) > 0) and \
             (suppl_life_enrollment is None or len(suppl_life_enrollment) > 0) and \
             (ltd_enrollment is None or len(ltd_enrollment) > 0) and \
             (std_enrollment is None or len(std_enrollment) > 0):
            status = COMPLETED
        return status

    def has_no_benefits(self):
        return self.get_enrollment_status() == NO_BENEFITS
