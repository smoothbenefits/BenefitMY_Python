from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.service.employee_organization_service import EmployeeOrganizationService
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import EmployeeOrganizationSetupDataSerializer, EmployeeOrganizationSetupDataPostSerializer
from app.serializers.employee_organization.batch_employee_organization_setup_result_serializer \
    import BatchEmployeeOrganizationSetupResultSerializer


class BatchEmployeeOrganizationImportView(APIView):

    @transaction.atomic
    def post(self, request, company_id, format=None):
        serializer = EmployeeOrganizationSetupDataPostSerializer(data=request.DATA, many=True)
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data_list = serializer.object

        service = EmployeeOrganizationService()
        execute_result = service.batch_execute_employee_organization_setup(data_list)

        result_serializer = BatchEmployeeOrganizationSetupResultSerializer(execute_result)

        return Response(result_serializer.data)
