import boto3

class AwsMessagingService(object):
    def __init__(self):
        self._sns = boto3.resource('sns', region_name='us-west-2')

    def publish_message_to_topic(self, topic_name, message):
        topic = self._sns.Topic(topic_name)
        response = topic.publish(Message=message)
        return response
