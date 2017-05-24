from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_user_features import CompanyUserFeatures
from app.service.application_feature_service import ApplicationFeatureService


class CompleteCompanyUserApplicationFeaturesView(APIView):
    def get(self, request, company_id, user_id, format=None):
        appFeatureService = ApplicationFeatureService()
        complete_features = appFeatureService.get_complete_application_feature_status_by_company_user(company_id, user_id)
        return Response(complete_features)
