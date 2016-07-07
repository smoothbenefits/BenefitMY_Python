import responses
from django.conf import settings


class CertificateOfInsuranceAppMock(object):

    def setup_mock_get(self, path, return_json, return_status=200):
        response_path = '{0}{1}'.format(settings.COI_SERVICE_URL, path)
        responses.add(
            responses.GET,
            response_path,
            json=return_json,
            status=return_status,
            match_querystring=True)
