from rest_framework.views import APIView
from django.http import Http404

from app.models.person import Person
from app.serializers.person_serializer import PersonSerializer
from rest_framework.response import Response


class PersonView(APIView):
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response({'person': serializer.data})

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        person.delete()
        return Response({'deleted_person': serializer.data})

class PersonByUserView(APIView):
    def _get_object(self, user_id):
        try:
            return Person.objects.get(user=user_id, relationship='self')
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        person = self._get_object(user_id)
        serializer = PersonSerializer(person)
        return Response({'person': serializer.data})
