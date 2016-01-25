from app.serializers.dtos.operation_result_base_serializer \
    import OperationResultBaseSerializer
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import (EmployeeOrganizationSetupDataPostSerializer, EmployeeOrganizationSetupDataSerializer)


class EmployeeOrganizationSetupDataActionResultSerializer(OperationResultBaseSerializer):
    input_data = EmployeeOrganizationSetupDataPostSerializer()
    output_data = EmployeeOrganizationSetupDataSerializer()
