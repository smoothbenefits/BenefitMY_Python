from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.conf import settings

from app.serializers.person_serializer import PersonSerializer

from app.service.data_modification_service import DataModificationService

class CompanyUsersDataModificationSummaryView(APIView):

    '''
        @pk the company_id interested in
    '''
    def get(self, request, pk, format=None):
        mod_service = DataModificationService()

        company_user_persons = mod_service.employee_modifications_summary_person_info_only(pk, settings.DEFAULT_DATA_CHANGE_LOOKBACK_IN_MINUTES)
        serializer = PersonSerializer(company_user_persons,
                                        many=True)

        return Response({'company_users': serializer.data})
