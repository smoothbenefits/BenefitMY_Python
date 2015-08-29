from rest_framework import serializers
from app.serializers.view_models.employee_account_creation_info_serializer import EmployeeAccountCreationInfoSerializer
from app.view_models.batch_employee_account_creation_info import BatchEmployeeAccountCreationInfo


class BatchEmployeeAccountCreationInfoSerializer(serializers.Serializer):
    account_creation_info_list = EmployeeAccountCreationInfoSerializer(many=True)

    def restore_object(self, attrs, instance=None):
        return BatchEmployeeAccountCreationInfo(**attrs)
