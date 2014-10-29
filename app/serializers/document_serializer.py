from rest_framework import serializers

from user_serializer import UserSerializer
from company_serializer import CompanySerializer
from template_serializer import TemplateSerializer
from document_type_serializer import DocumentTypeSerializer
from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document


class CompanyDocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()
    template = TemplateSerializer()
    document_type = DocumentTypeSerializer()
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
