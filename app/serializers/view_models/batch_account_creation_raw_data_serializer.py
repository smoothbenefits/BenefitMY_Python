from rest_framework import serializers
from app.view_models.batch_account_creation_raw_data import BatchAccountCreationRawData

class BatchAccountCreationRawDataSerializer(serializers.Serializer):
    raw_data_list = serializers.CharField(many=True, required=False)
    send_email = serializers.BooleanField(required=False)

    def restore_object(self, attrs, instance=None):
        return BatchAccountCreationRawData(**attrs)
