from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.person import Person
from app.models.user import User
from app.serializers.user_serializer import UserSerializer
from app.serializers.person_serializer import PersonSerializer


class UserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UsersView(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserFamilyView(APIView):
    def get_families(self, pk):
        try:
            return Person.objects.filter(user=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        families = self.get_object(pk)
        serializer = PersonSerializer(families, many=True)
        return Response(serializer.data)
