from aws_event_message_publisher import AwsEventMessagePublisher
from aws_event_message_pump import AwsEventMessagePump


class AwsEventBusService(object):
    def __init__(self, aws_region=None):
        self._message_publisher = AwsEventMessagePublisher(aws_region)
        self._aws_region = aws_region

    def publish_event(self, event_object):
        return self._message_publisher.publish_event(event_object)

    def create_event_message_pump(self):
        return AwsEventMessagePump(self._aws_region)
