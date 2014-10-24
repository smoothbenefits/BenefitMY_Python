from rest_framework import serializers

from user_serializer import UserSerializer
from company_serializer import CompanySerializer
from template_serializer import TemplateSerializer
from document_type_serializer import DocumentTypeSerializer
from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    company = CompanySerializer()
    template = TemplateSerializer()
    document_type = DocumentTypeSerializer()
    document_field = DocumentFieldSerializer()

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
                  'document_field')
