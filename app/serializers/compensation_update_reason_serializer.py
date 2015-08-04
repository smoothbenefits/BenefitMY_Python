from rest_framework import serializers
from app.models.compensation_update_reason import CompensationUpdateReason
from hash_pk_serializer_base import HashPkSerializerBase

class CompensationUpdateReasonSerializer(HashPkSerializerBase):

    class Meta:
        model = CompensationUpdateReason
