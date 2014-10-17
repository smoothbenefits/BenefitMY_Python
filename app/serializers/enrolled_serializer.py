from rest_framework import serializers
from app.models.enrolled import Enrolled

from user_company_benefit_plan_option_serializer import \
    UserCompanyBenefitPlanOptionSerializer
from person_serializer import PersonSerializer

class EnrolledSerializer(serializers.ModelSerializer):

    benefits = UserCompanyBenefitPlanOptionSerializer()
    person = PersonSerializer(many=True)
    class Meta:

        model = Enrolled
