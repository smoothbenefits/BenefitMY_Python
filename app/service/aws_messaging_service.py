import boto3
from django.conf import settings

class AwsMessagingService(object):
    def __init__(self):
        region = settings.AMAZON_DEFAULT_REGION
        self._sns = boto3.resource('sns', region_name=region)

    def publish_message_to_topic(self, topic_resource_name, message):
        topic = self._sns.Topic(topic_resource_name)
        response = topic.publish(Message=message)
        return response
