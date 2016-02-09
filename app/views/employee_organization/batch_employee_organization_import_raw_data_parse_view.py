from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.service.employee_organization_service import EmployeeOrganizationService
from app.serializers.employee_organization.batch_employee_organization_import_raw_data_serializer \
    import BatchEmployeeOrganizationImportRawDataSerializer
from app.serializers.employee_organization.batch_employee_organization_import_raw_data_parse_result_serializer \
    import BatchEmployeeOrganizationImportRawDataParseResultSerializer


class BatchEmployeeOrganizationImportRawDataParseView(APIView):
    def post(self, request, company_id, format=None):
        serializer = BatchEmployeeOrganizationImportRawDataSerializer(data=request.DATA)
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        raw_data = serializer.object
        raw_data.company_id = company_id

        service = EmployeeOrganizationService()
        parse_result = service.parse_batch_employee_organization_import_raw_data(raw_data)

        result_serializer = BatchEmployeeOrganizationImportRawDataParseResultSerializer(parse_result)

        return Response(result_serializer.data)
