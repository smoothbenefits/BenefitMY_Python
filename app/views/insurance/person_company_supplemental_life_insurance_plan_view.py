from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from rest_framework import status
from app.models.insurance.person_comp_suppl_life_insurance_plan import \
    PersonCompSupplLifeInsurancePlan
from app.serializers.insurance.person_company_supplemental_life_insurance_plan_serializer import (
    PersonCompanySupplementalLifeInsurancePlanSerializer, 
    PersonCompanySupplementalLifeInsurancePlanPostSerializer)
from app.models.company_user import CompanyUser
from app.models.person import Person


class PersonCompanySupplementalLifeInsurancePlanView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return PersonCompSupplLifeInsurancePlan.objects.get(pk=pk)
        except PersonCompSupplLifeInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self._get_object(pk)
        serializer = PersonCompanySupplementalLifeInsurancePlanSerializer(plans)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = PersonCompanySupplementalLifeInsurancePlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = PersonCompanySupplementalLifeInsurancePlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyPersonsSupplementalLifeInsuranceView(APIView):
    """ benefit for all employees in a company """
    def _get_persons_id(self, pk):
        persons_id = []
        users = CompanyUser.objects.filter(company=pk,
                                           company_user_type='employee')
        for user in users:
            person = Person.objects.get(user=user.user_id)
            person_ids.append(person.id)
        return persons_id

    def _get_objects(self, persons_id):
        try:
            return PersonCompanySupplementalLifeInsurancePlanSerializer.objects.filter(person__in=persons_id)
        except PersonCompanySupplementalLifeInsurancePlanSerializer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        persons_id = self._get_users_id(pk)
        plans = self._get_objects(persons_id)
        serializer = PersonCompanySupplementalLifeInsurancePlanSerializer(plans, many=True)
        return Response(serializer.data)
