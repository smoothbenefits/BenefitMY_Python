from rest_framework import serializers
from app.models.user_company_waived_benefit import \
    UserCompanyWaivedBenefit
from company_serializer import CompanySerializer
from benefit_type_serializer import BenefitTypeSerializer


class UserCompanyWaivedBenefitSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    benefit_type = BenefitTypeSerializer()

    class Meta:
        model = UserCompanyWaivedBenefit
        depth = 1


class PostUserCompanyWaivedBenefitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompanyWaivedBenefit
