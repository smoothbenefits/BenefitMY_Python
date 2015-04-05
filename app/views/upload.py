import base64
import hmac, hashlib
import json
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.response import Response
from django.conf import settings


def _encode_key(company_id, user_id):
    raw_value = "{compid}__{uid}__{timestamp}".format(compid=company_id, uid=user_id, timestamp=datetime.utcnow())
    return base64.b64encode(raw_value)

@api_view(['GET'])
def get_upload_form_policy_and_signature(request, pk, user_id):
    ### We need translate PK, user_id and current time to a unique reversable key
    upload_document = json.dumps(settings.AMAZON_S3_UPLOAD_POLICY)
    upload_policy = base64.b64encode(upload_document)
    signature = base64.b64encode(hmac.new(settings.AMAZON_AWS_SECRET, upload_policy, hashlib.sha1).digest())
    meta = {'s3Host': settings.AMAON_S3_HOST,
            'policy': upload_policy, 
            'signature': signature, 
            'accessKey': settings.AMAZON_AWS_ACCESS_KEY_ID,
            'fileKey': _encode_key(pk, user_id)}
    return Response(meta)

class UploadView(APIView):
    def get(self, request, pk, format=None):
        return Response(status=status.HTTP_404_NOT_FOUND)
