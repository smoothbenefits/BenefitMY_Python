from rest_framework import serializers
from app.models.document_field import DocumentField
from hash_pk_serializer_base import HashPkSerializerBase


class DocumentFieldSerializer(HashPkSerializerBase):

    class Meta:
        model = DocumentField

