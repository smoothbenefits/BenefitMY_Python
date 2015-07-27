from rest_framework import serializers
from app.models.document_type import DocumentType
from hash_pk_serializer_base import HashPkSerializerBase


class DocumentTypeSerializer(HashPkSerializerBase):

    class Meta:
        model = DocumentType
