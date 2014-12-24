from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import transaction

from app.models.company import Company
from app.models.document_type import DocumentType
from app.models.template import Template
from app.serializers.template_serializer import TemplateSerializer
from app.service.user_document_generator import UserDocumentGenerator


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

    @transaction.atomic
    def put(self, request, pk, format=None):
        t = self.get_object(pk)
        try:
            d_type = DocumentType.objects.get(
                name=request.DATA['template']['document_type'])
        except DocumentType.DoesNotExist:
            d_type = DocumentType(name=request.DATA['template']['document_type'])
            d_type.save()
        t.company_id = request.DATA['company']
        t.document_type = d_type
        t.name = request.DATA['template']['name']
        t.content = request.DATA['template']['content']
        t.save()
        serializer = TemplateSerializer(t)
        return Response({'template': serializer.data})

    def delete(self, request, pk, format=None):
        if request.method == 'DELETE':
            t = self.get_object(pk)
            t.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TemplateFieldView(APIView):
    def get(self, request, pk, format=None):
        comp = Company.objects.get(pk=pk)
        if comp:
            generator = UserDocumentGenerator(comp, None)
            fields = generator.get_all_template_fields()
            ret_obj = []
            for key in fields:
                ret_obj.append({'key': key,'value':fields[key]})
            return Response(ret_obj)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@transaction.atomic
def templates(request):
    try:
        c = Company.objects.get(id=request.DATA['company'])
    except Company.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        d_type = DocumentType.objects.get(
            name=request.DATA['template']['document_type'])
    except DocumentType.DoesNotExist:
        d_type = DocumentType(name=request.DATA['template']['document_type'])

    t = Template(name=request.DATA['template']['name'],
                 content=request.DATA['template']['content'],
                 company=c,
                 document_type=d_type)
    d_type.save()
    t.save()

    serializer = TemplateSerializer(t)
    return Response({'template': serializer.data})
