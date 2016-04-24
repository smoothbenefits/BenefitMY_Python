from django.conf import settings
from ...action_base import ActionBase

from app.service.web_request_service import WebRequestService


class ActionCoiExpirationCheck(ActionBase):
    request_service = WebRequestService()

    API_URL_COI_EXPIRATION_CHECK = '{0}{1}'.format(
        settings.COI_SERVICE_URL,
        'api/v1/contractors/execute_insurance_validation'
    )

    def __init__(self):
        super(ActionCoiExpirationCheck, self).__init__()

    def execute(self, action_data):

        # Invoke the remote URL to trigger global timeoff accural
        r = self.request_service.post(
                self.API_URL_COI_EXPIRATION_CHECK,
                action_data)

        if (r.status_code != 200):
            self.log.error("Action {} failed to complete.".format(self.__class__.__name__))
            return

        self.log.info("Action {} ran to completion.".format(self.__class__.__name__))
