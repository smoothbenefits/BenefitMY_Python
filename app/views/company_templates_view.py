from rest_framework.views import APIView
from django.http import (
    Http404,
    HttpResponseForbidden)
from rest_framework.response import Response

from app.models.template import Template
from app.serializers.template_serializer import TemplateSerializer

from view_mixin import *


class CompanyTemplatesView(APIView, LoginRequiredMixin):
    def get_templates(self, pk):
        try:
            return Template.objects.filter(company=pk)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not is_employer(request.user.id, pk):
            return HttpResponseForbidden()

        templates = self.get_templates(pk)
        serializer = TemplateSerializer(templates,
                                        many=True)
        return Response({'templates': serializer.data})
