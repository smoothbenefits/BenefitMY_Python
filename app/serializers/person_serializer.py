from rest_framework import serializers
from app.models.person import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id',
                  'person_type',
                  'relationship',
                  'addresses',
                  'phones')

