from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.person import Person
from app.models.enrolled import Enrolled
from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.models.fsa.fsa_plan import FsaPlan
from app.models.hra.person_company_hra_plan import PersonCompanyHraPlan
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan

from app.serializers.enrolled_serializer import EnrolledSerializer
from app.serializers.user_company_waived_benefit_serializer import \
    UserCompanyWaivedBenefitSerializer
from app.serializers.fsa.fsa_serializer import FsaSerializer
from app.serializers.hra.person_company_hra_plan_serializer import \
    PersonCompanyHraPlanSerializer
from app.serializers.insurance.* import (
    PersonCompanySupplementalLifeInsurancePlanSerializer,
    UserCompanyLifeInsuranceSerializer,
    UserCompanyLtdInsuranceSerializer,
    UserCompanyStdInsuranceSerializer)

class PersonEnrollmentStatusView(APIView):
    """ Benefit enrollment status for a person """
    def get_user_id(self, person_id):
        try:
            person = Person.objects.get(pk=person_id)
            return person['user']
        except Person.DoesNotExist:
            raise Http404

    def get_health_benefit_enrollment(self, person_id):
        enrollment = Enrolled.objects.filter(person=person_id)
        serializer = EnrolledSerializer(enrollment, many=True, required=False)
        return serializer.data

    def get_health_benefit_waive(self, user_id):
        waived = UserCompanyWaivedBenefit(user=user_id)
        serializer = UserCompanyWaivedBenefitSerializer(waived, required=False)
        return serializer.data

    def get_hra_plan(self, person_id):
        hra_plan = PersonCompanyHraPlan.objects.filter(person=person_id)
        serializer = PersonCompanyHraPlanSerializer(hra_plan, required=False)
        return serializer.data

    def get_fsa_plan(self, user_id):
        fsa_plan = FsaPlan.objects.filter(user=user_id)
        serializer = FsaSerializer(fsa_plan, required=False)
        return serializer.data

    def get_life_insurance(self, user_id):
        life_insurance = UserCompanyLifeInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyLifeInsuranceSerializer(life_insurance, required=False)
        return serializer.data

    def get_supplimental_life_insurance(self, person_id):
        supplimental_life = PersonCompSupplLifeInsurancePlan.objects.filter(person=person_id)
        serializer = PersonCompanySupplementalLifeInsurancePlanSerializer(supplimental_life, required=False)
        return serializer.data

    def get_std_insurance(self, user_id):
        std_insurance = UserCompanyStdInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyStdInsuranceSerializer(std_insurance, required=False)
        return serializer.data

    def get_ltd_insurance(self, user_id):
        ltd_insurance = UserCompanyLtdInsurancePlan.objects.filter(user=user_id)
        serializer = UserCompanyLtdInsuranceSerializer(ltd_insurance, required=False)
        return serializer.data

    def get(self, request, person_id, format=None):
        user_id = self.get_user_id(person_id)

        health_benefit = self.get_health_benefit_enrollment(person_id)
        health_benefit_waived = self.get_health_benefit_waive(user_id)
        life_insurance = self.get_life_insurance(user_id)
        supplemental_life = self.get_supplimental_life_insurance(person_id)
        std_insurance = self.get_std_insurance(user_id)
        ltd_insurance = self.get_ltd_insurance(user_id)

        return Response({'benefits': serializer.data})
