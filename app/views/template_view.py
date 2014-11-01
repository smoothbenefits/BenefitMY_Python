from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from app.models.company import Company
from app.models.document_type import DocumentType
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
        return Response({'template': serializer.data})


@api_view(['POST'])
def templates(request):
    try:
        c = Company.objects.get(id=request.DATA['company'])
    except Company.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        d_type = DocumentType.objects.get(
            name=request.DATA['template']['document_type'])
    except Template.DoesNotExist:
        d_type = DocumentType(name=request.DATA['template']['document_type'])

    t = Template(name=request.DATA['template']['name'],
                 content=request.DATA['template']['content'],
                 company=c,
                 document_type=d_type)
    d_type.save()
    t.save()

    serializer = TemplateSerializer(t)
    return Response({'template': serializer.data})
