from rest_framework import serializers


class ValidationIssueSerializer(serializers.Serializer):
    severity = serializers.CharField()
    message = serializers.CharField()
