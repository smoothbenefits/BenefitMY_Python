from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from app.models.person import Person
from django.contrib.auth import get_user_model
from app.serializers.person_serializer import PersonSerializer, PersonFullPostSerializer
from rest_framework.response import Response
from app.serializers.user_serializer import UserFamilySerializer


User = get_user_model()


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

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonFullPostSerializer(person, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        person.delete()
        return Response({'deleted_person': serializer.data})

class FamilyByUserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_person_by_user(self, user, relation_to_user):
        try:
            person_set=Person.objects.filter(user=user, relationship=relation_to_user)
            if person_set:
                return person_set[0]
            else:
                return None
        except Person.DoesNotExist:
            return None


    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserFamilySerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        request.DATA['user'] = pk
        relationship = request.DATA['relationship']
        if relationship == 'spouse' or relationship == 'self':
            person = self.get_person_by_user(pk, relationship)
            if person:
                return Response({'message':'Cannot add a new {0} when you already have a {0} in DB'.format(relationship)}, 
                                status=status.HTTP_400_BAD_REQUEST)
        serializer = PersonFullPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
