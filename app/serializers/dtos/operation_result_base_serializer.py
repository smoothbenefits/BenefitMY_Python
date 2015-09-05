from rest_framework import serializers
from app.serializers.dtos.issue_serializer import IssueSerializer

class OperationResultBaseSerializer(serializers.Serializer):
    issues = IssueSerializer(many=True)
