from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.company import Company
from app.serializers.company_serializer import CompanySerializer


class CompanyView(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)
