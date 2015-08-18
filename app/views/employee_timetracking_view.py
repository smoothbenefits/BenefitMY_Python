from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.employee_timetracking import EmployeeTimeTracking
from app.serializers.employee_timetracking_serializer import (
    EmployeeTimeTrackingSerializer, EmployeeTimeTrackingPostSerializer)
from app.models.person import Person

class EmployeeTimeTrackingView(APIView):
    def _get_object(self, pk):
        try:
            return EmployeeTimeTracking.objects.get(pk=pk)
        except EmployeeTimeTracking.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee_timetracking = self._get_object(pk)
        serializer = EmployeeTimeTrackingSerializer(employee_timetracking)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        employee_timetracking = self._get_object(pk)
        employee_timetracking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):
        serializer = EmployeeTimeTrackingPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeTimeTrackingByPersonCompanyView(APIView):
    def _get_object(self, person_id):
        try:
            return EmployeeTimeTracking.objects.filter(person=person_id)
        except EmployeeTimeTracking.DoesNotExist:
            raise Http404

    def get(self, request, person_id, format=None):
        employee_timetracking = self._get_object(person_id)
        serializer = EmployeeTimeTrackingSerializer(employee_timetracking, many=True)
        return Response(serializer.data)
