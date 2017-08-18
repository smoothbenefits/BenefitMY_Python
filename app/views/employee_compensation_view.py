import json
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.employee_compensation import EmployeeCompensation
from app.serializers.employee_compensation_serializer import (
    EmployeeCompensationSerializer, EmployeeCompensationPostSerializer)
from app.service.compensation_service import CompensationService
from app.serializers.dtos.compensation_info_serializer import CompensationInfoSerializer
from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.service.event_bus.events.compensation_updated_event import CompensationUpdatedEvent


class EmployeeCompensationView(APIView):
    _aws_event_bus_service = AwsEventBusService()

    def _get_object(self, pk):
        try:
            return EmployeeCompensation.objects.get(pk=pk)
        except EmployeeCompensation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee_compensation = self._get_object(pk)
        serializer = EmployeeCompensationSerializer(employee_compensation)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        employee_compensation = self._get_object(pk)
        employee_compensation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):
        serializer = EmployeeCompensationPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()

            # Log event
            model = serializer.object
            self._aws_event_bus_service.publish_event(CompensationUpdatedEvent(model.person.user.id))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeCompensationByPersonView(APIView):
    def get(self, request, person_id, format=None):
        comp_service = CompensationService(person_id)
        all_comps = comp_service.get_all_compensation_ordered()
        serializer = CompensationInfoSerializer(all_comps, many=True)
        return Response(serializer.data)
