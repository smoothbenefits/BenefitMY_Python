from rest_framework import serializers
from app.models.template import Template
from company_serializer import ShallowCompanySerializer
from document_type_serializer import DocumentTypeSerializer
from hash_pk_serializer_base import HashPkSerializerBase

import re


class TemplateSerializer(HashPkSerializerBase):
    fields = serializers.SerializerMethodField('find_fields')

    def find_fields(self, foo):
        field_names = re.findall('{{(.*?)}}', foo.content)
        for field_name in field_names:
            yield {'name': field_name}

    company = ShallowCompanySerializer()
    document_type = DocumentTypeSerializer()

    class Meta:
        model = Template
        fields = ("id", "company", "document_type", "name", "content", "fields")
