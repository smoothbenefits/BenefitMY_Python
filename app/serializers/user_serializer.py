from rest_framework import serializers
from app.models.user import User
from app.models.person import Person
from app.serializers.person_serializer import PersonSerializer


class UserSerializer(serializers.ModelSerializer):
    """ we only use person model first/last name
    """
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')

    def get_first_name(self, foo):
        p = Person.objects.get(user=foo.id)
        return p.first_name

    def get_last_name(self, foo):
        p = Person.objects.get(user=foo.id)
        return p.last_name

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
