from rest_framework import serializers
from app.models.signature import Signature


class SignatureSerializer(serializers.ModelSerializer):

    class Meta:

        model = Signature
