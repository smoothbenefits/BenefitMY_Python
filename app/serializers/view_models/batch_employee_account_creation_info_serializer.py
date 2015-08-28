from rest_framework import serializers
from app.serializers.view_models.employee_account_creation_info_serializer import EmployeeAccountCreationInfoSerializer


class BatchEmployeeAccountCreationInfoSerializer(serializers.Serializer):
    account_creation_info_list = EmployeeAccountCreationInfoSerializer(many=True)
    send_email = serializers.BooleanField()
