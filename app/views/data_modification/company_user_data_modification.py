from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404

from app.serializers.person_serializer import PersonSerializer

from app.service.data_modification_service import DataModificationService

class CompanyUsersDataModificationSummaryView(APIView):

    '''
        @pk the company_id interested in
    '''
    def get(self, request, pk, format=None):
        mod_service = DataModificationService()

        company_user_persons = mod_service.employee_modifications_summary_person_info_only(pk, 10)
        serializer = PersonSerializer(company_user_persons,
                                        many=True)

        mod_service.employee_modifications_notify_employer_for_all_companies(10)

        return Response({'company_users': serializer.data})