from .aws_event_message_facility_base import AwsEventMessageFacilityBase
from .aws_event_message_utility import AwsEventMessageUtility


class AwsEventMessagePublisher(AwsEventMessageFacilityBase):
    def __init__(self, aws_region=None):
        super(AwsEventMessagePublisher, self).__init__(aws_region)

    def publish_event(self, event_object):
        AwsEventMessageUtility.validate_event_object(event_object)

        topic_name = AwsEventMessageUtility.get_sns_topic_name(type(event_object))
        topic_arn = AwsEventMessageUtility.ensure_sns_topic(self._sns, topic_name)
        response = self._sns.publish(
            TopicArn=topic_arn,
            Message=event_object.serialize())

        return response
    