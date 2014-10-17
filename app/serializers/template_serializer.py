from rest_framework import serializers
from app.models.template import Template

from app.serializer.company_serializer import CompanySerializer
from app.serializer.document_type_serializer import DocumentTypeSerializer


class TemplateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Template
