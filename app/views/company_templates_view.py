from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.template import Template
from app.serializers.template_serializer import CompanyTemplatesSerializer


class CompanyTemplatesView(APIView):
    def get_templates(self, pk):
        try:
            return Template.objects.filter(company=pk)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        templates = self.get_templates(pk)
        serializer = CompanyTemplatesSerializer(templates, many=True)
        return Response({'templates':serializer.data})
