from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from django.db import transaction
from app.models.health_benefits.enrolled import Enrolled
from app.models.health_benefits.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.health_benefits.user_company_benefit_plan_option_serializer import (
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
        # Get the update reason off of the request
        recordReason = request.DATA['record_reason']

        for benefit in request.DATA['benefits']:
            u = UserCompanyBenefitPlanOption(
                    user_id=pk,
                    benefit_id=benefit['benefit']['id'],
                    record_reason_id=recordReason['record_reason_id'],
                    record_reason_note=recordReason['record_reason_note'])
            u.save()
            for enroll in benefit["enrolleds"]:
                p_id = enroll['id']
                if 'pcp' in enroll:
                    pcp = enroll['pcp']
                else:
                    pcp = ''
                enrolled = Enrolled(user_company_benefit_plan_option=u,
                                    person_id=p_id,
                                    pcp=pcp)
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
    def _get_user_ids(self, pk):
        user_ids = []
        users = CompanyUser.objects.filter(company=pk,
                                           company_user_type='employee')
        for user in users:
            user_ids.append(user.user_id)
        return user_ids

    def _get_objects(self, user_ids):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user__in=user_ids)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        user_ids = self._get_user_ids(pk)
        plans = self._get_objects(user_ids)
        serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
        return Response({'benefits': serializer.data})
