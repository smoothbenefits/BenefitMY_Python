from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_benefit_plan_option import CompanyBenefitPlanOption
from app.serializers.company_benefit_plan_option_serializer import (
    CompanyBenefitPlanOptionSerializer,
    CompanyBenefitPlanOptionPostSerializer,
    CompanyBenefitPlanSerializer)


class CompanyBenefitPlanOptionView(APIView):
    def get_object(self, pk):
        try:
            return CompanyBenefitPlanOption.objects.get(pk=pk)
        except CompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan_option = self.get_object(pk)
        serializer = CompanyBenefitPlanOptionSerializer(plan_option)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CompanyBenefitPlanOptionPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyBenefitPlansView(APIView):
    def get_object(self, pk):
        try:
            return CompanyBenefitPlanOption.objects.filter(company=pk)
        except CompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self.get_object(pk)
        serializer = CompanyBenefitPlanSerializer(plans, many=True)
        return Response({'benefits':serializer.data})
