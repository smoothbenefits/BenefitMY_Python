from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_group import CompanyGroup
from app.serializers.company_group_serializer import (
    CompanyGroupSerializer,
    CompanyGroupPostSerializer)


class CompanyGroupView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyGroup.objects.get(pk=pk)
        except CompanyGroup.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        group = CompanyGroup.objects.filter(company=company_id)
        serializer = CompanyGroupSerializer(Group, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = CompanyGroupPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        company_group = self._get_object(pk)
        serializer = CompanyGroupSerializer(company_group, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self._get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
