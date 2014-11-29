from rest_framework import serializers
from app.models.user import User
from app.serializers.person_serializer import PersonSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email')


class UserFamilySerializer(serializers.ModelSerializer):

    family = PersonSerializer(many=True)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'family')
