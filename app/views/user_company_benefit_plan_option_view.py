from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status


from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.user_company_benefit_plan_option_serializer import (
    UserCompanyBenefitPlanOptionSerializer,
    UserBenefitPostSerializer)


class UserCompanyBenefitPlanOptionView(APIView):
    def get_object(self, pk):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user=pk)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self.get_object(pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
        return Response({'benefits': serializer.data})

    def post(self, request, pk, format=None):
        serializer = UserBenefitPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
