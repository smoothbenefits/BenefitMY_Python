from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.extra_benefits.person_company_extra_benefit_plan import \
    PersonCompanyExtraBenefitPlan
from app.serializers.extra_benefits.person_company_extra_benefit_plan_serializer import (
    PersonCompanyExtraBenefitPlanSerializer,
    PersonCompanyExtraBenefitPlanPostSerializer)


class PersonCompanyExtraBenefitPlanView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return PersonCompanyExtraBenefitPlan.objects.get(pk=pk)
        except PersonCompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = PersonCompanyExtraBenefitPlanSerializer(plan)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = PersonCompanyExtraBenefitPlanPostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        serializer = PersonCompanyExtraBenefitPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonCompanyExtraBenefitPlanByPersonView(APIView):
    """ Commuter plan enrollment for a single employee """
    def _get_object(self, person_id):
        try:
            return PersonCompanyExtraBenefitPlan.objects.filter(person=person_id)
        except PersonCompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, person_id, format=None):
        plans = self._get_object(person_id)
        serializer = PersonCompanyExtraBenefitPlanSerializer(plans, many=True)
        return Response(serializer.data)
