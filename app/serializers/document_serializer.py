from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document


class CompanyDocumentSerializer(serializers.ModelSerializer):
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
                  'fields')
        depth = 1


class UserDocumentSerializer(serializers.ModelSerializer):
    fields = DocumentFieldSerializer()

    class Meta:
        model = Document
        depth = 1
        fileds = ('id',
                  'name',
                  'content',
                  'edited',
                  'company',
                  'user',
                  'template'
                  'document_type',
                  'fields')
