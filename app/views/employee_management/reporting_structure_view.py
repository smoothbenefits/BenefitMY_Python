from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.person import Person
from app.models.company_user import CompanyUser
from app.models.employee_profile import EmployeeProfile
from app.serializers.company_user_serializer import (
    CompanyUserSerializer, CompanyUserDetailSerializer)
from app.service.company_personnel_service import CompanyPersonnelService


class DirectReportsView(APIView):

    _personnel_service = CompanyPersonnelService()

    def get(self, request, comp_id, user_id, format=None):
        direct_reports = self._personnel_service.get_direct_report_company_users(comp_id, user_id)
        serializer = CompanyUserSerializer(direct_reports, many=True)
        return Response({'user_roles':serializer.data})
