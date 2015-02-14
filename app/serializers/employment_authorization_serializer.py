from rest_framework import serializers
from app.models.employment_authorization import EmploymentAuthorization

from signature_serializer import SignatureSerializer
from hash_pk_serializer_base import HashPkSerializerBase


class EmploymentAuthorizationSerializer(HashPkSerializerBase):

    signature = SignatureSerializer()

    class Meta:

        model = EmploymentAuthorization
