from rest_framework import serializers
from app.dtos.key_value_pair import KeyValuePair


class KeyValuePairSerializer(serializers.Serializer):
    key = serializers.CharField(required=False)
    value = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        return KeyValuePair(**attrs)
