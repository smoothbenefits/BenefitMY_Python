from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.user_company_waived_benefit import UserCompanyWaivedBenefit
from app.serializers.user_company_waived_benefit_serializer import (
    UserCompanyWaivedBenefitSerializer,
    PostUserCompanyWaivedBenefitSerializer)


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
        request.DATA['user'] = pk
        serializer = PostUserCompanyWaivedBenefitSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
