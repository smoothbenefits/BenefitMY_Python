from rest_framework import serializers
from app.models.user_company_waived_benefit import \
    UserCompanyWaivedBenefit


class WaivedBenefitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompanyWaivedBenefit
