from rest_framework import serializers
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField
from app.models.onboarding.user_onboarding_step_state \
    import UserOnboardingStepState


class UserOnboardingStepStateSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")

    class Meta:
        model = UserOnboardingStepState


class UserOnboardingStepStatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOnboardingStepState
