from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.employment_authorization import EmploymentAuthorization
from app.serializers.employment_authorization_serializer import (
    EmploymentAuthorizationSerializer,
    EmploymentAuthorizationPostSerializer)


class EmploymentAuthorizationView(APIView):
    def get_object(self, pk):
        try:
            return EmploymentAuthorization.objects.get(user=pk)
        except EmploymentAuthorization.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ea = self.get_object(pk)
        serializer = EmploymentAuthorizationSerializer(ea)
        return Response(serializer.data)

    def post(self, request, pk, format=None):

        request.DATA['user'] = pk
        try:
            ea = EmploymentAuthorization.objects.get(user=pk)
            serializer = EmploymentAuthorizationPostSerializer(ea,
                                                           data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except EmploymentAuthorization.DoesNotExist:
            serializer = EmploymentAuthorizationPostSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
