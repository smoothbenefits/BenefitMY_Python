from rest_framework import serializers
from app.models.enrolled import Enrolled
from person_serializer import PersonSerializer


class EnrolledSerializer(serializers.ModelSerializer):

    person = PersonSerializer()

    class Meta:

        model = Enrolled
