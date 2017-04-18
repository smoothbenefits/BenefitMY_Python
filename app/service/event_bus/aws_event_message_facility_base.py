import boto3

from django.conf import settings
from .events.event_base import EventBase
from .event_handlers.event_handler_base import EventHandlerBase
from .aws_client import AwsClient

class AwsEventMessageFacilityBase(object):
    def __init__(self, aws_region=None):
        if (not aws_region):
            aws_region = settings.DEFAULT_AWS_REGION
        self._aws_client = AwsClient(
            aws_region=aws_region,
            aws_access_key_id=settings.AMAZON_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON_AWS_SECRET
        )
