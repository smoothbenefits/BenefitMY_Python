import base64
import hmac, hashlib
import json
from urlparse import urlparse
from datetime import datetime, timedelta
from django.conf import settings

'''
This is the service to provide various authentication strings for Amazon S3.
'''

class AmazonS3AuthService(object):
    
    def encode_key(self, company_id, user_id):
        raw_value = "{compid}__{uid}__{timestamp}".format(compid=company_id, uid=user_id, timestamp=datetime.utcnow())
        return base64.b64encode(raw_value)


    def get_s3_key(self, company_name, file_name, file_key):
        file_relative = '{0}:{1}:{2}'.format(company_name, file_key, file_name)
        return file_relative.replace(" ", "_")


    def get_upload_form_policy_and_signature(self, s3_key):
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


    def get_s3_request_datetime(self):
        return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")


    def get_s3_request_auth(self, request_method, content_type, file_path, cur_time):
        string_to_sign = '{0}\n\n\n{1}\n{2}\n{3}'.format(request_method, 
                                                       content_type, 
                                                       "x-amz-date:"+ cur_time, 
                                                       "/" + settings.AMAZON_S3_BUCKET + file_path)
        signature = base64.b64encode(hmac.new(settings.AMAZON_AWS_SECRET, string_to_sign, hashlib.sha1).digest())
        return "AWS" + " " + settings.AMAZON_AWS_ACCESS_KEY_ID + ":" + signature;


    def get_s3_full_url(self, s3_path):
        return settings.AMAZON_S3_HOST + s3_path
