from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.sys_period_definition import SysPeriodDefinition
from app.serializers.sys_period_definition_serializer import SysPeriodDefinitionSerializer

class SysPeriodDefinitionView(APIView):
    def get(self, request, format=None):
        defs = SysPeriodDefinition.objects.all()
        serialized = SysPeriodDefinitionSerializer(defs, many=True)
        return Response(serialized.data)