from rest_framework import serializers
from app.models.template import Template

import re


class TemplateSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField('find_fields')

    def find_fields(self, foo):
        field_names = re.findall('{{(.*?)}}', foo.content)
        for field_name in field_names:
            yield {'name': field_name}

    class Meta:
        model = Template
        fields = ("id", "company", "document_type", "name", "content", "fields")
        depth = 1

