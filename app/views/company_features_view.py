from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_features import CompanyFeatures
from app.serializers.company_features_serializer import (
    CompanyFeaturesSerializer,
    CompanyFeaturesPostSerializer)
from app.service.application_feature_service import ApplicationFeatureService


class CompanyFeaturesView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyFeatures.objects.get(pk=pk)
        except CompanyFeatures.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        features = CompanyFeatures.objects.filter(company=pk)
        serializer = CompanyFeaturesSerializer(features, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CompanyFeaturesPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        company_feature = self._get_object(pk)
        serializer = CompanyFeaturesSerializer(company_feature, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        f = self._get_object(pk)
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CompleteCompanyApplicationFeaturesView(APIView):
    def get(self, request, company_id, format=None):
        appFeatureService = ApplicationFeatureService()
        complete_features = appFeatureService.get_complete_application_feature_status_by_company(company_id)
        return Response(complete_features)
