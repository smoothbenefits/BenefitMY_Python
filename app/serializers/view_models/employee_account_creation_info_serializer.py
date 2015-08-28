from rest_framework import serializers
from app.serializers.custom_fields.hash_field import HashField
from app.serializers.compensation_info_serializer import CompensationInfoSerializer
from app.serializers.view_models.validation_issue_serializer import ValidationIssueSerializer
from app.view_models.employee_account_creation_info import EmployeeAccountCreationInfo
from app.serializers.view_models.key_value_pair_serializer import KeyValuePairSerializer

class EmployeeAccountCreationInfoSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    company_id = serializers.IntegerField()
    company_user_type = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    employment_type = serializers.CharField()
    compensation_info = CompensationInfoSerializer(required=False)
    send_email = serializers.BooleanField()
    password = serializers.CharField(required=False)
    create_docs = serializers.BooleanField()
    doc_fields = KeyValuePairSerializer(many=True)
    validation_issues = ValidationIssueSerializer(many=True, required=False)

    def restore_object(self, attrs, instance=None):
        return EmployeeAccountCreationInfo(**attrs)
