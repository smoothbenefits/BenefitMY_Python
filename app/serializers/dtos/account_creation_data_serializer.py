from rest_framework import serializers
from app.serializers.custom_fields.hash_field import HashField
from app.serializers.dtos.compensation_info_serializer import CompensationInfoSerializer
from app.dtos.account_creation_data import AccountCreationData
from app.serializers.dtos.key_value_pair_serializer import KeyValuePairSerializer


class AccountCreationDataSerializer(serializers.Serializer):
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

    def restore_object(self, attrs, instance=None):
        return AccountCreationData(**attrs)
