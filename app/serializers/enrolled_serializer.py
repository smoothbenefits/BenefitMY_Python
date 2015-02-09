from rest_framework import serializers
from app.models.enrolled import Enrolled
from person_serializer import PersonSerializer
from hash_pk_serializer_base import HashPkSerializerBase


class EnrolledSerializer(HashPkSerializerBase):

    person = PersonSerializer()

    class Meta:

        model = Enrolled
