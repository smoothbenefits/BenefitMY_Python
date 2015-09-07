from rest_framework import serializers
from app.dtos.batch_account_creation_raw_data import BatchAccountCreationRawData


class BatchAccountCreationRawDataSerializer(serializers.Serializer):
    raw_data = serializers.CharField()
    send_email = serializers.BooleanField()

    def restore_object(self, attrs, instance=None):
        return BatchAccountCreationRawData(**attrs)
