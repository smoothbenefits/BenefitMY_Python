from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    fields = DocumentFieldSerializer()

    class Meta:
        model = Document
        fileds = ('id',
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
        fileds = ('name',
                  'content',
                  'template'
                  'document_type',
                  'fields')
        depth = 1
