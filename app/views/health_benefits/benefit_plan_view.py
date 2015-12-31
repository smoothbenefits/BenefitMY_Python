from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.db import transaction
from app.models.health_benefits.benefit_plan import BenefitPlan
from app.serializers.health_benefits.benefit_plan_serializer import BenefitPlanSerializer, BenefitPlanPostSerializer

TYPE = {"Medical": 1,
        "Dental": 2,
        "Vision": 3}


class BenefitPlanView(APIView):
    def get_object(self, pk):
        try:
            return BenefitPlan.objects.get(pk=pk)
        except BenefitPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        benefit_plan = self.get_object(pk)
        serializer = BenefitPlanSerializer(benefit_plan)
        return Response({'benefit': serializer.data})

    def delete(self, request, pk, format=None):
        benefit_plan = self.get_object(pk)
        if benefit_plan:
            benefit_plan_serialized = BenefitPlanSerializer(benefit_plan)
            benefit_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BenefitPlanCreationView(APIView):

    def post(self, request, format=None):
        if (not "benefit_type" in request.DATA or
            not "benefit_name" in request.DATA or
            not "mandatory_pcp" in request.DATA):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        benefit_data = {
            "name": request.DATA["benefit_name"],
            "benefit_type": TYPE[request.DATA['benefit_type']],
            "mandatory_pcp": request.DATA["mandatory_pcp"]
        }

        if 'pcp_link' in request.DATA:
            benefit_data['pcp_link'] = request.DATA['pcp_link']


        serializer = BenefitPlanPostSerializer(data=benefit_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'benefit':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
