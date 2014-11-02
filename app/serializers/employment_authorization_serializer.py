from rest_framework import serializers
from app.models.employment_authorization import EmploymentAuthorization

from signature_serializer import SignatureSerializer


class EmploymentAuthorizationSerializer(serializers.ModelSerializer):

    signature = SignatureSerializer()

    class Meta:

        model = EmploymentAuthorization
