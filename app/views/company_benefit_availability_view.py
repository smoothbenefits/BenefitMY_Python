import json
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.company import Company
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from app.models.hra.company_hra_plan import CompanyHraPlan
from app.models.hsa.company_hsa_plan import CompanyHsaPlan
from app.models.insurance.comp_suppl_life_insurance_plan import \
    CompSupplLifeInsurancePlan
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan
from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan

from app.serializers.company_serializer import CompanySerializer
from app.serializers.company_benefit_plan_option_serializer import \
    CompanyBenefitPlanOptionSerializer
from app.serializers.fsa.company_fsa_plan_serializer import CompanyFsaPlanSerializer
from app.serializers.hra.company_hra_plan_serializer import \
    CompanyHraPlanSerializer
from app.serializers.hsa.company_hsa_plan_serializer import \
    CompanyHsaPlanSerializer
from app.serializers.insurance.company_supplemental_life_insurance_plan_serializer import \
    CompanySupplementalLifeInsurancePlanSerializer
from app.serializers.insurance.company_life_insurance_plan_serializer import \
    CompanyLifeInsurancePlanSerializer
from app.serializers.insurance.company_ltd_insurance_plan_serializer import \
    CompanyLtdInsurancePlanSerializer
from app.serializers.insurance.company_std_insurance_plan_serializer import \
    CompanyStdInsurancePlanSerializer

class CompanyBenefitAvailabilityView(APIView):
    """ Benefit availability for a company """

    def get_company_info(self, company_id):
        try:
            company = Company.objects.get(pk=company_id)
            serializer = CompanySerializer(company)
            return serializer.data
        except Company.DoesNotExist:
            raise Http404

    def get_health_benefit(self, company_id):
        healthBenefit = CompanyBenefitPlanOption.objects.filter(company=company_id)
        serializer = CompanyBenefitPlanOptionSerializer(healthBenefit, many=True, required=False)
        return serializer.data

    def get_hra_plan(self, company_id):
        hra_plan = CompanyHraPlan.objects.filter(company=company_id)
        serializer = CompanyHraPlanSerializer(hra_plan, required=False, many=True)
        return serializer.data

    def get_hsa_plan(self, company_id):
        hsa_plan = CompanyHsaPlan.objects.filter(company=company_id)
        serializer = CompanyHsaPlanSerializer(hsa_plan, required=False, many=True)
        return serializer.data

    def get_fsa_plan(self, company_id):
        fsa_plan = CompanyFsaPlan.objects.filter(company=company_id)
        serializer = CompanyFsaPlanSerializer(fsa_plan, required=False, many=True)
        return serializer.data

    def get_life_insurance(self, company_id):
        life_insurance = CompanyLifeInsurancePlan.objects.filter(company=company_id)
        serializer = CompanyLifeInsurancePlanSerializer(life_insurance, required=False, many=True)
        return serializer.data

    def get_supplimental_life_insurance(self, company_id):
        supplimental_life = CompSupplLifeInsurancePlan.objects.filter(company=company_id)
        serializer = CompanySupplementalLifeInsurancePlanSerializer(supplimental_life, required=False, many=True)
        return serializer.data

    def get_std_insurance(self, company_id):
        std_insurance = CompanyStdInsurancePlan.objects.filter(company=company_id)
        serializer = CompanyStdInsurancePlanSerializer(std_insurance, required=False, many=True)
        return serializer.data

    def get_ltd_insurance(self, company_id):
        ltd_insurance = CompanyLtdInsurancePlan.objects.filter(company=company_id)
        serializer = CompanyLtdInsurancePlanSerializer(ltd_insurance, required=False, many=True)
        return serializer.data

    def get(self, request, company_id, format=None):
        company_info = self.get_company_info(company_id)

        health_benefit = self.get_health_benefit(company_id)
        medical, dental, vision = [], [], []
        for benefit in health_benefit:
            if benefit['benefit_plan']['benefit_type']['name'] == 'Medical':
                medical.append(benefit)
            if benefit['benefit_plan']['benefit_type']['name'] == 'Dental':
                dental.append(benefit)
            if benefit['benefit_plan']['benefit_type']['name'] == 'Vision':
                vision.append(benefit)

        hra_plan = self.get_hra_plan(company_id)
        fsa_plan = self.get_fsa_plan(company_id)
        hsa_plan = self.get_hsa_plan(company_id)
        life_insurance = self.get_life_insurance(company_id)
        supplemental_life = self.get_supplimental_life_insurance(company_id)
        std_insurance = self.get_std_insurance(company_id)
        ltd_insurance = self.get_ltd_insurance(company_id)

        response = {
            "company": company_info,
            "medical": medical,
            "dental": dental,
            "vision": vision,
            "hra": hra_plan,
            "fsa": fsa_plan,
            "hsa": hsa_plan,
            "basic_life": life_insurance,
            "supplemental_life": supplemental_life,
            "std": std_insurance,
            "ltd": ltd_insurance
        }

        return Response(response)
