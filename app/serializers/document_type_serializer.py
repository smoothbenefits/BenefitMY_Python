from rest_framework import serializers
from app.models.document_type import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType

