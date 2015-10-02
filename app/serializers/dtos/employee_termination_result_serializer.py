from app.serializers.dtos.operation_result_base_serializer import OperationResultBaseSerializer
from app.serializers.dtos.employee_termination_data_serializer import EmployeeTerminationDataSerializer
from app.serializers.employee_profile_serializer import EmployeeProfileSerializer


class EmployeeTerminationResultSerializer(OperationResultBaseSerializer):
    input_data = EmployeeTerminationDataSerializer()
    output_data = EmployeeProfileSerializer()
