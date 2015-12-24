from rest_framework import serializers
from app.models.health_benefits.benefit_details import BenefitDetails
from benefit_plan_serializer import BenefitPlanSerializer
from benefit_policy_type_serializer import BenefitPolicyTypeSerializer
from benefit_policy_key_serializer import BenefitPolicyKeySerializer
from ..hash_pk_serializer_base import HashPkSerializerBase

class BenefitDetailsSerializer(HashPkSerializerBase):

	benefit_plan = BenefitPlanSerializer()
	benefit_policy_type = BenefitPolicyTypeSerializer()
	benefit_policy_key = BenefitPolicyKeySerializer()

	class Meta:
		model = BenefitDetails
		fields = ('id',
        		  'value',
                  'benefit_plan',
                  'benefit_policy_type',
                  'benefit_policy_key')
