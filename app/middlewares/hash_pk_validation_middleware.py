import re
import json
from io import BytesIO
from app.service.hash_key_service import HashKeyService
from django.http import Http404


class HashPkValidationMiddleware(object):

    def process_request(self, request):
        ''' Would also need to decode anything from the request post data, if it is JSON
        '''
        if ((request.method == 'POST' or request.method == 'PUT') and
                request.META.get('CONTENT_TYPE').find('application/json') >= 0):

            # find and decode all hashed keys from the post body
            body = re.sub(HashKeyService.HASH_TOKEN_REGEX_PATTERN,
                          lambda x: self._decode_value(x.group(0)), request.body)

            # according to the internals of the HttpRequest handling flow in Django Rest Framework and Django,
            # the below 2 acttributes need to be updated in order for the .DATA
            # parsing to properly reflect
            request._body = body
            request._stream = BytesIO(request._body)

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        ''' Don't like this much at all. We have to know the view arg names
            and to hard code in here, in order for the middle ware to know
            the ids needing "decoding". But how else we could wire these
            up given the current setup??

            This is another push to think about actually using non-int
        '''
        self._decode_key(view_kwargs, 'pk')
        self._decode_key(view_kwargs, 'pd')
        self._decode_key(view_kwargs, 'py')
        self._decode_key(view_kwargs, 'user_id')
        self._decode_key(view_kwargs, 'comp_id')
        self._decode_key(view_kwargs, 'feature_id')
        self._decode_key(view_kwargs, 'person_id')
        self._decode_key(view_kwargs, 'company_id')
        self._decode_key(view_kwargs, 'plan_id')
        self._decode_key(view_kwargs, 'company_group_id')
        self._decode_key(view_kwargs, 'document_id')

        return None

    def process_response(self, request, response):
        ''' Would need to encode anything in the response data, if it is JSON
        '''
        if (request.method == 'PUT' and response.content):
            res = json.loads(response.content)
            self._encode_key('person', res)
            self._encode_key('company', res)
            self._encode_key('company_group', res)
            self._encode_key('user', res)

            response.content = json.dumps(res)

        return response

    def _decode_key(self, view_kwargs, key_name):
        if (key_name in view_kwargs):
            k = self._decode_value(view_kwargs[key_name])
            if (not k):
                raise Http404
            view_kwargs[key_name] = k

    def _decode_value(self, value):
        hash_key_service = HashKeyService()
        return hash_key_service.decode_key(value)

    def _encode_key(self, key, response):
        if key in response:
            response[key] = self._encode_value(response[key])

    def _encode_value(self, value):
        hash_key_service = HashKeyService()
        if not hash_key_service.is_encoded(value):
            return hash_key_service.encode_key(value)

        return value
