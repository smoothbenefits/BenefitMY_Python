from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService

User = get_user_model()


API_URL_COI = '{0}{1}'.format(
    settings.COI_SERVICE_URL,
    'api/v1'
)


class ContratorService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()

    def get_contractor_by_id(self, contractor_id):
        api_url = '{0}/contractor/{1}'.format(
                        API_URL_COI,
                        contractor_id)

        # Make the request and parse the response as json
        r = self.request_service.get(api_url)
        entry = r.json()

        return entry
