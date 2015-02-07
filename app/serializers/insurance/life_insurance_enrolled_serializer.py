from rest_framework import serializers
from app.models.insurance.life_insurance_enrolled import LifeInsuranceEnrolled
from person_serializer import PersonSerializer


class LifeInsuranceEnrolledSerializer(serializers.ModelSerializer):

    person = PersonSerializer()

    class Meta:

        model = LifeInsuranceEnrolled
