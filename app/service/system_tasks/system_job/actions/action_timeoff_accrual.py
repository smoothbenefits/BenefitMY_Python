import json
from django.conf import settings
from ...action_base import ActionBase

from app.service.aws_messaging_service import AwsMessagingService


class ActionTimeoffAccural(ActionBase):
    messageing_service = AwsMessagingService()

    def __init__(self):
        super(ActionTimeoffAccural, self).__init__()

    def execute(self, action_data):;
        # Invoke the remote URL to trigger global timeoff accural
        r = self.messageing_service.publish_message_to_topic(
            settings.AMAZON_TIME_ACCURAL_TOPIC,
            json.dumps(action_data)
        )
        response = json.loads(r)

        if (!r.MessageId):
            self.log.error("Action {} failed to complete.".format(self.__class__.__name__))
            return

        self.log.info("Action {} ran to completion. Message id {}".format(self.__class__.__name__, r.MessageId))
