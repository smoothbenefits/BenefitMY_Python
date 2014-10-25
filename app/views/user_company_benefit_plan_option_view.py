from rest_framework.views import APIView
from django.http import Http404

from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.user_company_benefit_plan_option_serializer import \
    UserCompanyBenefitPlanOptionSerializer
from rest_framework.response import Response


class UserCompanyBenefitPlanOptionView(APIView):
    def get_object(self, pk):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user=pk)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self.get_object(pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
        return Response(serializer.data)
