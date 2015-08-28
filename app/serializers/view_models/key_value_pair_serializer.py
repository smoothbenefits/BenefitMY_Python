from rest_framework import serializers
from app.view_models.key_value_pair import KeyValuePair

class KeyValuePairSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        return KeyValuePair(**attrs)
