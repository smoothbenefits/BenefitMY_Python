import requests


class WebRequestService(object):

    # Disable the request warnings
    requests.packages.urllib3.disable_warnings()

    def get(self, url, qs_params=None, auth_token=None):
        if (not qs_params):
            qs_params = {}

        return requests.get(
            url,
            params=qs_params,
            headers=self._get_headers(auth_token),
            verify=False)

    def post(self, url, data_object, qs_params=None, auth_token=None):
        if (not qs_params):
            qs_params = {}

        return requests.post(
            url,
            json=data_object,
            params=qs_params,
            headers=self._get_headers(auth_token),
            verify=False)

    def put(self, url, data_object, qs_params=None, auth_token=None):
        if (not qs_params):
            qs_params = {}

        return requests.put(
            url,
            json=data_object,
            params=qs_params,
            headers=self._get_headers(auth_token),
            verify=False)

    def _get_headers(self, auth_token):
        headers = {}
        if (auth_token):
            headers['Authorization'] = 'Bearer {0}'.format(auth_token)
        
        return headers
