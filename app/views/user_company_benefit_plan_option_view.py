from rest_framework.views import APIView
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from app.models.enrolled import Enrolled
from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.serializers.user_company_benefit_plan_option_serializer import (
    UserCompanyBenefitPlanOptionSerializer,
    UserBenefitPostSerializer)

DICT={'Medical': 1,
      'Dental': 2,
      'Vision': 3}

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


@api_view(['POST'])
def user_select_benefit(request, pk, pc):
    for benefit in request.DATA['benefits']:
        enroll_list = [ids["id"] for ids in benefit["enrolleds"] ]
        try:
            benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
            for b in benefits:
                if (DICT[benefit['benefit']['benefit_type']] ==
                    b.benefit.benefit_plan.benefit_type_id):
                    # update
                    b.benefit_id=benefit['benefit']['id']
                    b.save()


                    break

            else:
                # insert
                u = UserCompanyBenefitPlanOption(user_id=pk,
                    benefit_id=benefit['benefit']['id'])
                u.save()

        # No benefit exists for the user
        except UserCompanyBenefitPlanOption.DoesNotExist:
            u = UserCompanyBenefitPlanOption(user_id=pk,
                    benefit_id=benefit['benefit']['id'])
            u.save()



        benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(benefits, many=True)
        return Response({'benefits': serializer.data})
