from rest_framework import serializers
from app.models.template import Template


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template

