from rest_framework import serializers
from app.models.template import Template

from app.serializers.document_type_serializer import DocumentTypeSerializer


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        depth = 1



