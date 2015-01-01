from rest_framework import serializers
from app.models.user import User
from app.models.person import Person
from app.serializers.person_serializer import PersonSerializer


class UserSerializer(serializers.ModelSerializer):
    """ we only use person model first/last name
    """
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')

    def _get_self_person(self, input_user):
      try:
          p = Person.objects.get(user=input_user.id, relationship='self')
          return p
      except Person.DoesNotExist:
        return None

    def get_first_name(self, input_user):
      self_person = self._get_self_person(input_user)
      if self_person:
        return self_person.first_name
      else:
        return ""

    def get_last_name(self, input_user):
      self_person = self._get_self_person(input_user)
      if self_person:
        return self_person.last_name
      else:
        return ""

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
