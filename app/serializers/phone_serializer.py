from rest_framework import serializers
from app.models.phone import Phone


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = ('id',
                  'phone_type',
                  'number')

