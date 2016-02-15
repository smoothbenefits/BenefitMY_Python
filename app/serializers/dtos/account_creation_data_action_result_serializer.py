from app.serializers.dtos.operation_result_base_serializer import OperationResultBaseSerializer
from app.serializers.dtos.account_creation_data_serializer import AccountCreationDataSerializer


class AccountCreationDataActionResultSerializer(OperationResultBaseSerializer):
    input_data = AccountCreationDataSerializer()
    output_data = AccountCreationDataSerializer()
