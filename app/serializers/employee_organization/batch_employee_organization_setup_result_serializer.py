from app.serializers.dtos.operation_result_base_serializer \
    import OperationResultBaseSerializer
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import EmployeeOrganizationSetupDataSerializer
from app.serializers.employee_organization.employee_organization_setup_data_action_result_serializer \
    import EmployeeOrganizationSetupDataActionResultSerializer

class BatchEmployeeOrganizationSetupResultSerializer(OperationResultBaseSerializer):
    input_data = EmployeeOrganizationSetupDataSerializer(many=True)
    output_data = EmployeeOrganizationSetupDataActionResultSerializer(many=True)
