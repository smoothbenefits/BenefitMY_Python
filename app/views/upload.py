import base64
import hmac, hashlib
import json
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from app.models.upload import Upload
from app.serializers.upload_serializer import UploadSerializer



def _encode_key(company_id, user_id):
    raw_value = "{compid}__{uid}__{timestamp}".format(compid=company_id, uid=user_id, timestamp=datetime.utcnow())
    return base64.b64encode(raw_value)

@api_view(['GET'])
def get_upload_form_policy_and_signature(request, pk, user_id):
    ### We need translate PK, user_id and current time to a unique reversable key
    _expiration = datetime.utcnow() + timedelta(hours=5)
    settings.AMAZON_S3_UPLOAD_POLICY.update({"expiration": _expiration.strftime("%Y-%m-%dT%H:%M:%SZ")})
    upload_document = json.dumps(settings.AMAZON_S3_UPLOAD_POLICY)

    upload_policy = base64.b64encode(upload_document)
    signature = base64.b64encode(hmac.new(settings.AMAZON_AWS_SECRET, upload_policy, hashlib.sha1).digest())
    meta = {'s3Host': settings.AMAZON_S3_HOST,
            'policy': upload_policy, 
            'signature': signature, 
            'accessKey': settings.AMAZON_AWS_ACCESS_KEY_ID,
            'fileKey': _encode_key(pk, user_id)}
    return Response(meta)

class UploadView(APIView):
    def _get_object(self, pk, comp_id):
        try:
            return Upload.objects.get(pk=pk, company=comp_id)
        except Upload.DoesNotExist:
            raise Http404

    def _get_by_user(self, user_id, comp_id):
        try:
            return Upload.objects.filter(user=user_id, company=comp_id)
        except Upload.DoesNotExist:
            raise Http404

    def get(self, request, comp_id, pk, format=None):
        uploads = self._get_by_user(pk, comp_id)
        serialized = UploadSerializer(uploads, many=True) 
        return Response(serialized.data)

    def post(self, request, comp_id, pk, format=None):
        upload_data = request.DATA
        serialized = UploadSerializer(data=upload_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comp_id, pk, format=None):
        upload = self._get_object(pk, comp_id)
        if upload:
            upload.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
