from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.service.employee_management_service import EmployeeManagementService
from app.serializers.dtos.employee_termination_data_serializer import EmployeeTerminationDataSerializer
from app.serializers.dtos.employee_termination_result_serializer import EmployeeTerminationResultSerializer


class EmployeeTerminationView(APIView):

    @transaction.atomic
    def post(self, request, company_id, format=None):
        serializer = EmployeeTerminationDataSerializer(data=request.DATA)
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee_termiation_data = serializer.object

        service = EmployeeManagementService()
        operation_result = service.terminate_employee(employee_termiation_data)

        result_serializer = EmployeeTerminationResultSerializer(operation_result)

        return Response(result_serializer.data)
