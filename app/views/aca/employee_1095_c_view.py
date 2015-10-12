from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.db import transaction
from rest_framework.response import Response
from app.models.aca.employee_1095_c import Employee1095C
from app.serializers.aca.employee_1095_c_serializer import \
    Employee1095CSerializer, Employe1095CPostSerializer
from app.models.company import Company
from app.models.person import Person

class Employee1095CView(APIView):
    def _get_objects(self, person_id, company_id):
        return Employee1095C.objects.filter(person=person_id, company=company_id)

    def _validate_company_id(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def _validate_person_id(self, person_id):
        try:
            return Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, person_id, company_id, format=None):
        self._validate_company_id(company_id)
        self._validate_person_id(person_id)
        employee_1095c = self._get_objects(person_id, company_id)
        serialized = Employee1095CSerializer(employee_1095c, many=True)
        return Response(serialized.data)

    @transaction.atomic
    def post(self, request, person_id, company_id, format=None):
        self._validate_company_id(company_id)
        self._validate_person_id(person_id)
        serialized = Employe1095CPostSerializer(data=request.DATA, many=True)
        if serialized.is_valid():
            # Delete all existing company fields
            employee_1095c_array = self._get_objects(person_id, company_id)
            employee_1095c_array.delete()
            # Save all the new ones
            serialized.save()
            return Response({'saved': serialized.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
