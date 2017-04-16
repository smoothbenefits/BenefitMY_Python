from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.employee_profile import EmployeeProfile
from app.serializers.employee_profile_serializer import (
    EmployeeProfileSerializer, EmployeeProfilePostSerializer, EmployeeProfileWithNameSerializer)
from app.models.person import Person
from django.db.models import Q
from app.service.integration.company_integration_provider_data_service \
import CompanyIntegrationProviderDataService


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
        serializer = EmployeeProfilePostSerializer(employee_profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()

            # [TODO]: To remove
            # This is setup to test the integration data sync
            integration_data_service = CompanyIntegrationProviderDataService()
            employee_user_id = employee_profile.person.user.id
            integration_data_service.sync_employee_data_to_remote(employee_user_id)

            response_serializer = EmployeeProfileSerializer(serializer.object)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = EmployeeProfilePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            response_serializer = EmployeeProfileSerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeProfileByPersonCompanyView(APIView):
    def _get_object(self, person_id, company_id):
        try:
            return EmployeeProfile.objects.get(person=person_id, company=company_id)
        except EmployeeProfile.DoesNotExist:
            raise Http404
    def get(self, request, person_id, company_id, format=None):
        employee_profile = self._get_object(person_id, company_id)
        serializer = EmployeeProfileSerializer(employee_profile)
        return Response(serializer.data)


class EmployeeProfileByCompanyUserView(APIView):
    def _get_object(self, company_id, user_id):
        try:
            person = Person.objects.get(user=user_id, relationship='self')
            return EmployeeProfile.objects.get(person=person.id, company=company_id)
        except (Person.DoesNotExist, EmployeeProfile.DoesNotExist):
            raise Http404

    def get(self, request, company_id, user_id, format=None):
        employee_profile = self._get_object(company_id, user_id)
        serializer = EmployeeProfileSerializer(employee_profile)
        return Response(serializer.data)


class EmployeeProfilesByCompanyView(APIView):
    def get(self, request, company_id, format=None):
        employee_profiles = EmployeeProfile.objects.filter(company=company_id)
        serializer = EmployeeProfileWithNameSerializer(employee_profiles, many=True)
        return Response(serializer.data)


class EmployeeProfileByCompanyPinView(APIView):
    def get(self, request, company_id, pin):
        try:
            # Employee's pin should be unique within the scope of a company
            employee_profile = EmployeeProfile.objects.get(company=company_id, pin=pin)
            serializer = EmployeeProfileSerializer(employee_profile)
            return Response(serializer.data)
        except EmployeeProfile.DoesNotExist:
            raise Http404
