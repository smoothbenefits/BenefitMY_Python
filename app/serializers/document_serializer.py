from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document
from app.models.document_field import DocumentField
import re


class DocumentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField('generate_content')
    fields = DocumentFieldSerializer()

    def generate_content(self, foo):
        content = foo.template.content
        if not content:
            content = foo.document_type.default_content
        field_names = re.findall('{{(.*?)}}', content)
        fields = DocumentField.objects.filter(document_id=foo.id)
        fields_dict = {f.name: f.value for f in fields}
        for f in field_names:
            if f in fields_dict:
                content = content.replace("{{%s}}" % f, fields_dict[f])

        return content

    class Meta:
        model = Document
        fields = ('id',
                  'name',
                  'edited',
                  'content',
                  'company',
                  'user',
                  'template',
                  'document_type',
                  'signature',
                  'fields')
        depth = 1
