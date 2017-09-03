from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from app.models.person import Person
from django.contrib.auth import get_user_model
from app.serializers.person_serializer import PersonSerializer, PersonFullPostSerializer
from rest_framework.response import Response
from app.serializers.user_serializer import UserFamilySerializer
from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.service.event_bus.events.person_info_updated_event import PersonInfoUpdatedEvent


User = get_user_model()


class PersonView(APIView):
    _aws_event_bus_service = AwsEventBusService()

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

            # Log event
            self._aws_event_bus_service.publish_event(PersonInfoUpdatedEvent(person.id))

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

    def is_person_associated_with_user(self, user, relation_to_user):
        person_set=Person.objects.filter(user=user, relationship=relation_to_user)
        return person_set.exists()


    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserFamilySerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        request.DATA['user'] = pk
        relationship = request.DATA['relationship']
        if relationship == 'spouse' or relationship == 'self':
            if self.is_person_associated_with_user(pk, relationship):
                return Response({'message':'Cannot add a new {0} when you already have a {0} in DB'.format(relationship)},
                                status=status.HTTP_400_BAD_REQUEST)
        serializer = PersonFullPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
