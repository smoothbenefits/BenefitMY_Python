from rest_framework import serializers


class IssueSerializer(serializers.Serializer):
    severity = serializers.CharField()
    message = serializers.CharField()
