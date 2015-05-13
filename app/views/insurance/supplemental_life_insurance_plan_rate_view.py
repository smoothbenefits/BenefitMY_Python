from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.insurance.supplemental_life_insurance_plan_rate import \
    SupplementalLifeInsurancePlanRate
from app.serializers.insurance.supplemental_life_insurance_plan_rate_serializer import (
    SupplementalLifeInsurancePlanRateSerializer, 
    SupplementalLifeInsurancePlanRatePostSerializer)


class SupplementalLifeInsurancePlanRateView(APIView):
    def _get_object(self, pk):
        try:
            return SupplementalLifeInsurancePlanRate.objects.get(pk=pk)
        except SupplementalLifeInsurancePlanRate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = SupplementalLifeInsurancePlanRateSerializer(plan)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = SupplementalLifeInsurancePlanRateSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = SupplementalLifeInsurancePlanRatePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplementalLifeInsurancePlanRateByPlanView(APIView):
    def _get_object(self, plan_id):
        try:
            return SupplementalLifeInsurancePlanRate.objects.filter(supplemental_life_insurance_plan=plan_id)
        except SupplementalLifeInsurancePlanRate.DoesNotExist:
            raise Http404

    def get(self, request, plan_id, format=None):
        plans = self._get_object(plan_id)
        serializer = SupplementalLifeInsurancePlanRateSerializer(plans, many=True)
        return Response(serializer.data)
