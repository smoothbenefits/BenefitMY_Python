from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.extra_benefits.company_extra_benefit_plan \
    import CompanyExtraBenefitPlan
from app.serializers.extra_benefits.company_extra_benefit_plan_serializer import (
    CompanyExtraBenefitPlanSerializer,
    CompanyExtraBenefitPlanPostSerializer)


class CompanyExtraBenefitPlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyExtraBenefitPlan.objects.get(pk=pk)
        except CompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyExtraBenefitPlanSerializer(plan)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyExtraBenefitPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyExtraBenefitPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyExtraBenefitPlanByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyExtraBenefitPlan.objects.filter(company=company_id)
        except CompanyExtraBenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        plans = self._get_object(company_id)
        serializer = CompanyExtraBenefitPlanSerializer(plans, many=True)
        return Response(serializer.data)
