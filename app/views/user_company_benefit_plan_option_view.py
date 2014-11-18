from rest_framework.views import APIView
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models.enrolled import Enrolled
from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.user_company_benefit_plan_option_serializer import (
    UserCompanyBenefitPlanOptionSerializer)


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
        _add_user_benefits(request, pk)
        benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(benefits, many=True)
        return Response({'benefits': serializer.data})


def _add_user_benefits(request, pk):
    for benefit in request.DATA['benefits']:
        enroll_list = [ids["id"] for ids in benefit["enrolleds"]]
        u = UserCompanyBenefitPlanOption(user_id=pk,
            benefit_id=benefit['benefit']['id'])
        u.save()
        for e in enroll_list:
            enrolled = Enrolled(user_company_benefit_plan_option=u,
                                person_id=e)
            enrolled.save()


@api_view(['PUT'])
def user_update_benefits(request, pk, pc):
    benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
    for b in benefits:
        if b.benefit.company_id == int(pc):
            Enrolled.objects.filter(
                user_company_benefit_plan_option=b.id).delete()
            b.delete()

    _add_user_benefits(request, pk)
    benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
    serializer = UserCompanyBenefitPlanOptionSerializer(benefits, many=True)
    return Response({'benefits': serializer.data})
