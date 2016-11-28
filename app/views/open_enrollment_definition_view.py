from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.open_enrollment_definition import OpenEnrollmentDefinition
from app.serializers.open_enrollment_definition_serializer import (
    OpenEnrollmentDefinitionSerializer,
    OpenEnrollmentDefinitionPostSerializer)


class OpenEnrollmentDefinitionByCompanyView(APIView):
    def _get_object(self, comp_id):
        try:
            return OpenEnrollmentDefinition.objects.get(company=comp_id)
        except OpenEnrollmentDefinition.DoesNotExist:
            raise Http404

    def get(self, request, comp_id, format=None):
        definition = self._get_object(comp_id)
        serializer = OpenEnrollmentDefinitionSerializer(definition)
        return Response(serializer.data)

    def post(self, request, comp_id, format=None):
        serializer = OpenEnrollmentDefinitionPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comp_id, format=None):
        definition = self._get_object(comp_id)
        serializer = OpenEnrollmentDefinitionPostSerializer(definition, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comp_id, format=None):
        definition = self._get_object(comp_id)
        definition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
