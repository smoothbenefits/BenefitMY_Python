from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from app.models.company_1095_c import Company1095C
from app.serializers.company_1095_c_serializer import Company1095CSerializer, Company1095CPostSerializer
from app.models.company import Company

class Company1095CView(APIView):
    def _get_objects(self, company_id):
        return Company1095C.objects.filter(company=company_id)

    def _validate_company_id(self, company_id):
        try:
            return Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        self._validate_company_id(pk)
        company_fields = self._get_objects(pk)
        serialized = Company1095CSerializer(company_fields, many=True)
        return Response(serialized.data)

    def post(self, request, pk, format=None):
        self._validate_company_id(pk)
        serialized = Company1095CPostSerializer(data=request.DATA, many=True)
        if serialized.is_valid():
            # Delete all existing company fields
            company_1095c_array = self._get_objects(pk)
            company_1095c_array.delete()
            # Save all the new ones
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
