from rest_framework import serializers
from app.custom_authentication import AuthUser as User
from app.models.person import Person
from app.serializers.person_serializer import PersonSerializer
from hash_pk_serializer_base import HashPkSerializerBase

class UserSerializer(HashPkSerializerBase):
    """ we only use person model first/last name
    """
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')

    def _get_self_person(self, input_user):
      try:
          p = Person.objects.filter(user=input_user.id, relationship='self')
          if p:
            return p[0]
          else:
            return None
      except Person.DoesNotExist:
        return None

    def _get_user(self, input_user):
        try:
            u = User.objects.get(pk=input_user.id)
            return u
        except User.DoesNotExist:
            return None

    def get_first_name(self, input_user):
        self_person = self._get_self_person(input_user)
        if self_person:
            return self_person.first_name
        else:
            user = self._get_user(input_user)
            if user:
                return user.first_name
            else:
                return ""

    def get_last_name(self, input_user):
        self_person = self._get_self_person(input_user)
        if self_person:
            return self_person.last_name
        else:
            user = self._get_user(input_user)
            if user:
                return user.last_name
            else:
                return ""

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email')


class UserFamilySerializer(HashPkSerializerBase):

    family = PersonSerializer(many=True)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'family')
