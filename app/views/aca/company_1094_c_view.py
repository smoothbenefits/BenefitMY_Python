from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.db import transaction
from rest_framework.response import Response
from app.models.aca.company_1094_c_member_info import Company1094CMemberInfo
from app.models.aca.company_1094_c_monthly_member_info import \
    Company1094CMonthlyMemberInfo
from app.serializers.aca.company_1094_c_member_info_serializer import \
    Company1094CMemberInfoSerializer, Company1094CMemberInfoPostSerializer
from app.serializers.aca.company_1094_c_monthly_member_info_serializer import \
    Company1094CMonthlyMemberInfoSerializer, Company1094CMonthlyMemberInfoPostSerializer
from app.models.company import Company

class Company1094CView(APIView):
    def _get_member_info(self, company_id):
        return Company1094CMemberInfo.objects.get(company=company_id)

    def _get_monthly_member_info(self, company_id):
        return Company1094CMonthlyMemberInfo.objects.filter(company=company_id)

    def _validate_company_id(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        self._validate_company_id(pk)
        member_info = self._get_member_info(pk)
        monthly_info = self._get_monthly_member_info(pk)
        serialized = Company1094CMemberInfoSerializer(member_info)
        serialized_monthly = Company1094CMonthlyMemberInfoSerializer(monthly_info, many=True)
        return Response({'member': serialized.data, 'monthly_info': serialized_monthly.data})

    @transaction.atomic
    def post(self, request, pk, format=None):
        saved = {}
        self._validate_company_id(pk)
        if ('member' in request.DATA):
            serialized = Company1094CMemberInfoPostSerializer(data=request.DATA['member'])
            if serialized.is_valid():
                existing_1094_c = self._get_member_info(pk)
                existing_1094_c.delete()
                serialized.save()
                saved['member'] = serialized.data
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        if ('monthly_info' in request.DATA):
            serialized_monthly = Company1094CMonthlyMemberInfoPostSerializer(data=request.DATA['monthly_info'])
            if serialized_monthly.is_valid():
                existing_1094_c_monthly = self._get_monthly_member_info(pk)
                existing_1094_c_monthly.delete()
                serialized_monthly.save()
                saved['monthly_info'] = serialized_monthly.data
            else:
                return Response(serialized_monthly.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(saved, status=status.HTTP_201_CREATED)
