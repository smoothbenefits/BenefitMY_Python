from rest_framework import serializers
from app.models.template import Template

from app.serializers.company_serializer import CompanySerializer
from app.serializers.document_type_serializer import DocumentTypeSerializer


class TemplateiPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = ("name",
                  "content",
                  "company",
                  "document_type")


class TemplateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Template


class CompanyTemplatesSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Template
