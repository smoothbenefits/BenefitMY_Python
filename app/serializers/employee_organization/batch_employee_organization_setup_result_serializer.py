from app.serializers.dtos.operation_result_base_serializer \
    import OperationResultBaseSerializer
from app.serializers.employee_organization.employee_organization_setup_data_serializer \
    import EmployeeOrganizationSetupDataSerializer
from app.serializers.employee_organization.employee_organization_setup_data_action_result_serializer \
    import EmployeeOrganizationSetupDataActionResultSerializer


''' Serialize out the result of the operation that batchly execute the list 
    of units of work that setup employee organization data. 
    input_data holds the list of data objects that hold data for the list of units
    of work.
    output_data holds the list of result objects corresponding to the execution of
    the list of units of work.
'''
class BatchEmployeeOrganizationSetupResultSerializer(OperationResultBaseSerializer):
    input_data = EmployeeOrganizationSetupDataSerializer(many=True)
    output_data = EmployeeOrganizationSetupDataActionResultSerializer(many=True)
