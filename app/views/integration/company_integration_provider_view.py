from rest_framework.views import APIView
from django.http import Http404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from app.service.integration.integration_provider_service import IntegrationProviderService


class CompanyIntegrationProvidersByCompanyView(APIView):

    def get(self, request, company_id, format=None):
        service = IntegrationProviderService()
        result = service.get_company_integration_providers(company_id)
        return Response(result)
