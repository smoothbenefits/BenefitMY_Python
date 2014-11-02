from rest_framework import serializers
from app.models.signature_authorization import Signature


class SignatureSerializer(serializers.ModelSerializer):

    class Meta:

        model = Signature
