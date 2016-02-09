from app.serializers.dtos.operation_result_base_serializer \
    import OperationResultBaseSerializer
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import (EmployeeOrganizationSetupDataPostSerializer, EmployeeOrganizationSetupDataSerializer)


''' Serialize out the result of the operation that executes 1 unit (e.g. for one 
    employee) of employee organization setup. 
    input_data holds the data object of the unit of work before the operation
    output_data holds the data object of the unit of work after the operation
'''
class EmployeeOrganizationSetupDataActionResultSerializer(OperationResultBaseSerializer):
    input_data = EmployeeOrganizationSetupDataPostSerializer()
    output_data = EmployeeOrganizationSetupDataSerializer()
