from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.template import Template
from app.serializers.template_serializer import TemplateSerializer


class TemplateView(APIView):
    def get_object(self, pk):
        try:
            return Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)
