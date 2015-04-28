from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.employee_profile import EmployeeProfile
from app.serializers.employee_profile_serializer import (
    EmployeeProfileSerializer, EmployeeProfilePostSerializer)

class EmployeeProfileView(APIView):
    def _get_object(self, pk):
        try:
            return EmployeeProfile.objects.get(pk=pk)
        except EmployeeProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee_profile = self._get_object(pk)
        serializer = EmployeeProfileSerializer(employee_profile)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        employee_profile = self._get_object(pk)
        employee_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        employee_profile = self._get_object(pk)
        serializer = EmployeeProfileSerializer(employee_profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = EmployeeProfilePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeProfileByPersonView(APIView):
    def _get_object(self, person_id):
        try:
            return EmployeeProfile.objects.get(person=person_id)
        except EmployeeProfile.DoesNotExist:
            raise Http404
    def get(self, request, person_id, format=None):
        employee_profile = self._get_object(person_id)
        serializer = EmployeeProfileSerializer(employee_profile)
        return Response(serializer.data)
