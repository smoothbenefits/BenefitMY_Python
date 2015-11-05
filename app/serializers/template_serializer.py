from rest_framework import serializers
from app.models.template import Template
from company_serializer import ShallowCompanySerializer
from hash_pk_serializer_base import HashPkSerializerBase
from upload_serializer import UploadSerializer

import re


class TemplateSerializer(HashPkSerializerBase):
    fields = serializers.SerializerMethodField('find_fields')

    def find_fields(self, foo):
        field_names = re.findall('{{(.*?)}}', foo.content)
        for field_name in field_names:
            yield {'key': field_name}

    company = ShallowCompanySerializer()
    upload = UploadSerializer()

    class Meta:
        model = Template
        fields = ("id", "company", "name", "content", "fields", "upload")
