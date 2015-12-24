from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from app.service.hash_key_service import HashKeyService

from app.models.person import Person
from app.models.health_benefits.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.models.health_benefits.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.fsa.fsa import FSA
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.hsa.person_company_group_hsa_plan import PersonCompanyGroupHsaPlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan

from app.serializers.person_serializer import PersonSerializer
from app.serializers.health_benefits.user_company_benefit_plan_option_serializer import \
    UserCompanyBenefitPlanOptionSerializer
from app.serializers.health_benefits.user_company_waived_benefit_serializer import \
    UserCompanyWaivedBenefitSerializer
from app.serializers.fsa.fsa_serializer import FsaSerializer
from app.serializers.hra.person_company_hra_plan_serializer import \
    PersonCompanyHraPlanSerializer
from app.serializers.hsa.person_company_group_hsa_plan_serializer import \
    PersonCompanyGroupHsaPlanSerializer
from app.serializers.insurance.person_company_supplemental_life_insurance_plan_serializer import \
    PersonCompanySupplementalLifeInsurancePlanSerializer
from app.serializers.insurance.user_company_life_insurance_serializer import \
    UserCompanyLifeInsuranceSerializer
from app.serializers.insurance.user_company_ltd_insurance_serializer import \
    UserCompanyLtdInsuranceSerializer
from app.serializers.insurance.user_company_std_insurance_serializer import \
    UserCompanyStdInsuranceSerializer

class PersonEnrollmentSummaryView(APIView):
    """ Benefit enrollment status for a person """
    def __init__(self):
        self.hash_service = HashKeyService()

    def get_person_info(self, person_id):
        try:
            person = Person.objects.get(pk=person_id)
            serializer = PersonSerializer(person)
            return serializer.data
        except Person.DoesNotExist:
            raise Http404

    def get_health_benefit_enrollment(self, user_id):
        enrollment = UserCompanyBenefitPlanOption.objects.filter(user=user_id)
        serializer = UserCompanyBenefitPlanOptionSerializer(enrollment, many=True, required=False)
        return serializer.data

    def get_health_benefit_waive(self, user_id):
        waived = UserCompanyWaivedBenefit.objects.filter(user=user_id)
        serializer = UserCompanyWaivedBenefitSerializer(waived, required=False, many=True)
        return serializer.data

    def get_hra_plan(self, person_id):
        hra_plan = PersonCompanyHraPlan.objects.filter(person=person_id)
        serializer = PersonCompanyHraPlanSerializer(hra_plan, required=False, many=True)
        return serializer.data

    def get_fsa_plan(self, user_id):
        fsa_plan = FSA.objects.filter(user=user_id)
        serializer = FsaSerializer(fsa_plan, required=False, many=True)
        return serializer.data

    def get_hsa_plan(self, person_id):
        hsa_plan = PersonCompanyGroupHsaPlan.objects.filter(person=person_id)
        serializer = PersonCompanyGroupHsaPlanSerializer(hsa_plan, required=False, many=True)
        return serializer.data

    def get_life_insurance(self, user_id):
        life_insurance = UserCompanyLifeInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyLifeInsuranceSerializer(life_insurance, required=False, many=True)
        return serializer.data

    def get_supplimental_life_insurance(self, person_id):
        supplimental_life = PersonCompSupplLifeInsurancePlan.objects.filter(person=person_id)
        serializer = PersonCompanySupplementalLifeInsurancePlanSerializer(supplimental_life, required=False, many=True)
        return serializer.data

    def get_std_insurance(self, user_id):
        std_insurance = UserCompanyStdInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyStdInsuranceSerializer(std_insurance, required=False, many=True)
        return serializer.data

    def get_ltd_insurance(self, user_id):
        ltd_insurance = UserCompanyLtdInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyLtdInsuranceSerializer(ltd_insurance, required=False, many=True)
        return serializer.data

    def get(self, request, person_id, format=None):
        person_info = self.get_person_info(person_id)
        user_id = self.hash_service.decode_key(person_info['user'])

        health_benefit = self.get_health_benefit_enrollment(user_id)
        health_benefit_waived = self.get_health_benefit_waive(user_id)
        hra_plan = self.get_hra_plan(person_id)
        fsa_plan = self.get_fsa_plan(user_id)
        hsa_plan = self.get_hsa_plan(person_id)
        life_insurance = self.get_life_insurance(user_id)
        supplemental_life = self.get_supplimental_life_insurance(person_id)
        std_insurance = self.get_std_insurance(user_id)
        ltd_insurance = self.get_ltd_insurance(user_id)

        response = {
            "person" : person_info,
            "health_benefit_enrolled" : health_benefit,
            "health_benefit_waived" : health_benefit_waived,
            "hra" : hra_plan,
            "fsa" : fsa_plan,
            "hsa" : hsa_plan,
            "basic_life" : life_insurance,
            "supplemental_life" : supplemental_life,
            "std" : std_insurance,
            "ltd" : ltd_insurance
        }

        return Response(response)
