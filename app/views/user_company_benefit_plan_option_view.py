from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from django.db import transaction
from app.models.enrolled import Enrolled
from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.user_company_benefit_plan_option_serializer import (
    UserCompanyBenefitPlanOptionSerializer)
from app.models.company_user import CompanyUser


class UserCompanyBenefitPlanOptionView(APIView):
    """ single employee benefit """
    def get_object(self, pk):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user=pk)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self.get_object(pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
        return Response({'benefits': serializer.data})

    def _add_user_benefits(self, request, pk):
        for benefit in request.DATA['benefits']:
            enroll_list = [ids["id"] for ids in benefit["enrolleds"]]
            if 'pcp' in benefit['benefit'] and benefit['benefit']['pcp']:
                pcp_id = benefit['benefit']['pcp']
            else:
                pcp_id = ''
            u = UserCompanyBenefitPlanOption(
                    user_id=pk,
                    benefit_id=benefit['benefit']['id'],
                    pcp = pcp_id)
            u.save()
            for e in enroll_list:
                enrolled = Enrolled(user_company_benefit_plan_option=u,
                                    person_id=e)
                enrolled.save()

    @transaction.atomic
    def post(self, request, pk, format=None):
        benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
        for b in benefits:
            Enrolled.objects.filter(
                user_company_benefit_plan_option=b.id).delete()
            b.delete()
        self._add_user_benefits(request, pk)
        benefits = UserCompanyBenefitPlanOption.objects.filter(user=pk)
        serializer = UserCompanyBenefitPlanOptionSerializer(benefits, many=True)
        return Response({'benefits': serializer.data})


class CompanyUsersBenefitPlanOptionView(APIView):
    """ benefit for all employees in a company """
    def _get_users_id(self, pk):
        users_id = []
        users = CompanyUser.objects.filter(company=pk,
                                           company_user_type='employee')
        for user in users:
            users_id.append(user.user_id)
        return users_id

    def _get_objects(self, users_id):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user__in=users_id)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        users_id = self._get_users_id(pk)
        plans = self._get_objects(users_id)
        serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
        return Response({'benefits': serializer.data})


