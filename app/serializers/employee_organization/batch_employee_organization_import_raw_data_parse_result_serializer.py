from app.serializers.dtos.operation_result_base_serializer \
    import OperationResultBaseSerializer
from app.serializers.employee_organization.batch_employee_organization_import_raw_data_serializer \
    import BatchEmployeeOrganizationImportRawDataSerializer
from app.serializers.employee_organization.employee_organization_setup_data_action_result_serializer \
    import EmployeeOrganizationSetupDataActionResultSerializer


''' Serialize (out to client) the result object of the action that 
    parses the raw text content, and corresponding validations.
    The input_data holds the original raw text data, which is the 
    input data to this operation. 
    The output_data holds a list of operation result object from the 
    validations of the list of operation data (i.e. one for each line
    of the original raw text data). This is to allow validation issue
    tracking on individule items as well as overall operation.   
'''
class BatchEmployeeOrganizationImportRawDataParseResultSerializer(OperationResultBaseSerializer):
    input_data = BatchEmployeeOrganizationImportRawDataSerializer()
    output_data = EmployeeOrganizationSetupDataActionResultSerializer(many=True)
