from rest_framework import serializers
from app.models.template import Template

import re


class TemplateSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField('find_fields')

    def find_fields(self, foo):
        return set(re.findall('{{(.*?)}}', foo.content))

    class Meta:
        model = Template
        fields = ("company", "document_type", "name", "content", "fields")
        depth = 1
