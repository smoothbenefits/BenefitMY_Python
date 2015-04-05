import base64
import hmac, hashlib
import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.response import Response
from django.conf import settings


@api_view(['GET'])
def get_upload_form_policy_and_signature(request):
    if not (request.user or request.user.id > 0):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    upload_document = json.dumps(settings.AMAZON_S3_UPLOAD_POLICY)
    upload_policy = base64.b64encode(upload_document)
    signature = base64.b64encode(hmac.new(settings.AMAZON_AWS_SECRET, upload_policy, hashlib.sha1).digest())
    return Response({'policy': upload_policy, 'signature': signature, 'accessKey': settings.AMAZON_AWS_ACCESS_KEY_ID})

class UploadView(APIView):
    def get(self, request, pk, format=None):
        return Response(status=status.HTTP_404_NOT_FOUND)
