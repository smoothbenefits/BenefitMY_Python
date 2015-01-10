from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.serializers.user_company_waived_benefit_serializer import (
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
        try:
            waived_benefit = UserCompanyWaivedBenefit.objects.get(
                user_id=pk,
                company_id=request.DATA['company'],
                benefit_type_id=request.DATA['benefit_type'])
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except UserCompanyWaivedBenefit.DoesNotExist:
            w = UserCompanyWaivedBenefit(
                user_id=pk,
                company_id=request.DATA['company'],
                benefit_type_id=request.DATA['benefit_type'])

            w.save()

        serializer = UserCompanyWaivedBenefitSerializer(w)
        return Response(serializer.data)


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
