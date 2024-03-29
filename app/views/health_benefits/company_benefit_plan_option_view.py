from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.db import transaction
from app.models.health_benefits.benefit_plan import BenefitPlan
from app.models.health_benefits.company_benefit_plan_option import CompanyBenefitPlanOption
from app.serializers.health_benefits.company_benefit_plan_option_serializer import (
    CompanyBenefitPlanOptionSerializer,
    CompanyBenefitPlanOptionPostSerializer,
    CompanyBenefitPlanSerializer)
from app.serializers.health_benefits.benefit_plan_serializer import BenefitPlanSerializer


class CompanyBenefitPlanOptionView(APIView):
    def get_object(self, pk):
        try:
            return CompanyBenefitPlanOption.objects.get(pk=pk)
        except CompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan_option = self.get_object(pk)
        serializer = CompanyBenefitPlanOptionSerializer(plan_option)
        return Response({'benefit': serializer.data})

    def delete(self, request, pk, format=None):
        benefit_plan = BenefitPlan.objects.get(pk=pk)
        if benefit_plan:
            benefit_plan_serialized = BenefitPlanSerializer(benefit_plan)
            benefit_plan.delete()
            return Response({'benefit': benefit_plan_serialized.data})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@transaction.atomic
def create_benefit_plan_option(request):
    if (not "company" in request.DATA or
        not "benefit" in request.DATA or
        not "benefit_plan_id" in request.DATA["benefit"] or
        not "benefit_option_type" in request.DATA["benefit"] or
        not "total_cost_per_period" in request.DATA["benefit"] or
        not "employee_cost_per_period" in request.DATA["benefit"]):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    company_benefits = CompanyBenefitPlanOption.objects.filter(
        company=request.DATA['company'])

    if company_benefits:
        for b in company_benefits:
            if (b.benefit_option_type == request.DATA['benefit']['benefit_option_type'] and
                b.benefit_plan.id == request.DATA['benefit']['benefit_plan_id']):
                return Response(status=status.HTTP_409_CONFLICT)

    company_data = {
        "company": request.DATA["company"],
        "benefit_option_type": request.DATA["benefit"]["benefit_option_type"],
        "total_cost_per_period": request.DATA["benefit"]["total_cost_per_period"],
        "employee_cost_per_period": request.DATA["benefit"]["employee_cost_per_period"],
        "benefit_plan": request.DATA["benefit"]["benefit_plan_id"]
    }

    serializer = CompanyBenefitPlanOptionPostSerializer(data=company_data)
    if serializer.is_valid():
        serializer.save()
        response_serializer = CompanyBenefitPlanOptionSerializer(serializer.object)
        return Response({'benefits': response_serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyBenefitPlansView(APIView):
    def get_object(self, pk):
        try:
            return CompanyBenefitPlanOption.objects.filter(company=pk).order_by('benefit_plan')
        except CompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self.get_object(pk)
        serializer = CompanyBenefitPlanSerializer(plans, many=True)
        return Response({'benefits': serializer.data})
