from rest_framework import serializers
from app.models.w4 import W4


class W4Serializer(serializers.ModelSerializer):

    class Meta:

        model = W4
