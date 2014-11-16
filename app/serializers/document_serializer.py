from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document
from app.models.document_type import DocumentType
import re

class DocumentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField('generate_content')

    def generate_content(self, foo):
        content = foo.template.content
        field_names = re.findall('{{(.*?)}}', foo.content)
        fields = DocumentType.object.filter(document_id=foo.id)
        for f in field_names:
            content.replace("{{%s}}" % f, "{{%}}" % fields[f])

        return content



    fields = DocumentFieldSerializer()

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
