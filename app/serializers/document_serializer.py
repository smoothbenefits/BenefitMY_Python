from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    fields = DocumentFieldSerializer()

    class Meta:
        model = Document
        fields = ('id',
                  'name',
                  'content',
                  'edited',
                  'company',
                  'user',
                  'template'
                  'document_type',
                  'signature',
                  'fields')
        depth = 1


class TemplateDtypeSerializer(serializers.ModelSerializer):
    fields = DocumentFieldSerializer()

    class Meta:
        model = Document

        fields = ('template',
                  'fields')
        depth = 2
