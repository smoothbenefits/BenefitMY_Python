from django.db import transaction
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models.insurance.supplemental_life_insurance_plan import \
    SupplementalLifeInsurancePlan
from app.serializers.insurance.supplemental_life_insurance_plan_serializer import (
    SupplementalLifeInsurancePlanSerializer, 
    SupplementalLifeInsurancePlanPostSerializer)


class SupplementalLifeInsurancePlanView(APIView):
    def _get_object(self, pk):
        try:
            return SupplementalLifeInsurancePlan.objects.get(pk=pk)
        except SupplementalLifeInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self._get_object(pk)
        serializer = SupplementalLifeInsurancePlanSerializer(plans)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = SupplementalLifeInsurancePlanPostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        serializer = SupplementalLifeInsurancePlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
