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


@api_view(['GET'])
def _get_uploads_by_user(request, pk):
    try:
        user_uploads = Upload.objects.filter(user=pk)
        serialized = UploadSerializer(user_uploads, many=True)
        return Response(serialized.data)
    except Upload.DoesNotExist:
        raise Http404

class UploadView(APIView):
    def _get_object(self, pk, comp_id):
        try:
            return Upload.objects.get(pk=pk, company=comp_id)
        except Upload.DoesNotExist:
            raise Http404

    def _encode_key(self, company_id, user_id):
        raw_value = "{compid}__{uid}__{timestamp}".format(compid=company_id, uid=user_id, timestamp=datetime.utcnow())
        return base64.b64encode(raw_value)

    def _get_s3_key(self, company_name, file_name, file_key):
        file_relative = '{0}:{1}:{2}'.format(company_name, file_key, file_name)
        return file_relative.replace(" ", "_")


    def _get_upload_form_policy_and_signature(self, s3_key):
        expiration = datetime.utcnow() + timedelta(hours=5)
        settings.AMAZON_S3_UPLOAD_POLICY.update({"expiration": expiration.strftime("%Y-%m-%dT%H:%M:%SZ")})
        upload_document = json.dumps(settings.AMAZON_S3_UPLOAD_POLICY)

        upload_policy = base64.b64encode(upload_document)
        signature = base64.b64encode(hmac.new(settings.AMAZON_AWS_SECRET, upload_policy, hashlib.sha1).digest())
        return {
            's3Host': settings.AMAZON_S3_HOST,
            'policy':upload_policy,
            'signature': signature,
            'accessKey': settings.AMAZON_AWS_ACCESS_KEY_ID,
            'fileKey': s3_key, 
        }


    def get(self, request, comp_id,  pk, format=None):
        uploads = self._get_object(pk, comp_id)
        serialized = UploadSerializer(uploads) 
        return Response(serialized.data)


    def post(self, request, comp_id, pk, format=None):
        upload_data = request.DATA
        file_key = self._encode_key(comp_id, pk)
        s3_key = self._get_s3_key(upload_data['company_name'],
                                  upload_data['file_name'],
                                  file_key)
        upload_data.update({'S3': settings.AMAZON_S3_HOST + s3_key})
        upload_data.update({'company': comp_id})
        upload_data.update({'user': pk})
        serialized = UploadSerializer(data=upload_data)
        if serialized.is_valid():
            serialized.save()
            saved_upload = serialized.data
            saved_upload.update(self._get_upload_form_policy_and_signature(s3_key))
            return Response(saved_upload, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, comp_id, pk, format=None):
        upload = self._get_object(pk, comp_id)
        if upload:
            upload.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
