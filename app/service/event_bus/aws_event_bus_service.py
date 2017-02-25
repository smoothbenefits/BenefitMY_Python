import boto3

from django.conf import settings
from .events.event_base import EventBase


class AwsEventBusService(object):
    def __init__(self, aws_region=None):
        if (not aws_region):
            aws_region = settings.DEFAULT_AWS_REGION
        boto3.setup_default_session(
            aws_access_key_id=settings.AMAZON_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AMAZON_AWS_SECRET,
            region_name=aws_region)
        self._sns = boto3.client('sns')

    def publish_event(self, event_object):
        self._validate_event_object(event_object)

        topic_name = self._get_sns_topic_name(event_object)
        topic_arn = self._ensure_sns_topic(topic_name)
        response = self._sns.publish(
            TopicArn=topic_arn,
            Message=event_object.serialize())
        
        return response

    def _validate_event_object(self, event_object):
        if (not isinstance(event_object, EventBase)):
            raise Exception('The given object is not of the event type!')

    def _get_sns_topic_name(self, event_object):
        class_name = type(event_object).__name__
        return settings.ENVIRONMENT_IDENTIFIER + '_' + class_name

    def _ensure_sns_topic(self, topic_name):
        response = self._sns.create_topic(Name=topic_name)
        return response['TopicArn']
