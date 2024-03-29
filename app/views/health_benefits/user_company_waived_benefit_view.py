from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.health_benefits.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.serializers.health_benefits.user_company_waived_benefit_serializer import (
    UserCompanyWaivedBenefitSerializer)


class UserCompanyWaivedBenefitView(APIView):
    """ get/add user waived benefits
    """
    def get_object(self, pk):
        try:
            return UserCompanyWaivedBenefit.objects.filter(user=pk)
        except UserCompanyWaivedBenefit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        waived_benefit = self.get_object(pk)
        serializer = UserCompanyWaivedBenefitSerializer(
            waived_benefit, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        if 'company' in request.DATA:
        ### First delete all the waived records associated with the user
            comp_id = request.DATA['company']
            waived_benefits = UserCompanyWaivedBenefit.objects.filter(
                user_id=pk,
                company_id=comp_id)
            for existing_waived in waived_benefits:
                existing_waived.delete()

            # Get the update reason
            recordReason = request.DATA['record_reason']

            ### now save all the new waived records
            for input_waive in request.DATA['waived']:
                w = UserCompanyWaivedBenefit(
                    user_id=pk,
                    company_id=comp_id,
                    benefit_type_id=input_waive['benefit_type'],
                    reason=input_waive['reason'],
                    record_reason_id=recordReason['record_reason_id'],
                    record_reason_note=recordReason['record_reason_note'])

                w.save()
            return Response({'Success':'true'})
        else:
            return Response({'Success':'false', 'error': 'the request do not have \'company\' field specified'},
                            status=status.HTTP_400_BAD_REQUEST)

class CompanyWaivedBenefitView(APIView):
    """ get all waived benefits belong to a company
    """
    def get_object(self, pk):
        try:
            return UserCompanyWaivedBenefit.objects.filter(company=pk)
        except UserCompanyWaivedBenefit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        waived_benefit = self.get_object(pk)
        serializer = UserCompanyWaivedBenefitSerializer(
            waived_benefit, many=True)
        return Response(serializer.data)
