from django.conf import settings
from ...action_base import ActionBase

from app.service.web_request_service import WebRequestService


class ActionTimeoffAccural(ActionBase):
    request_service = WebRequestService()

    API_URL_TIMEOFF_ACCURAL = '{0}{1}'.format(
        settings.TIME_TRACKING_SERVICE_URL,
        'api/v1/timeoff_quotas/execute_accrual'
    )

    def __init__(self):
        super(ActionTimeoffAccural, self).__init__()

    def execute(self, action_data):
        # Invoke the remote URL to trigger global timeoff accural
        r = self.request_service.get(self.API_URL_TIMEOFF_ACCURAL)

        if (r.status_code != 200):
            self.log.error("Action {} failed to complete.".format(self.__class__.__name__))
            return

        self.log.info("Action {} ran to completion.".format(self.__class__.__name__))
