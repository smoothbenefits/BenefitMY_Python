from .aws_event_message_facility_base import AwsEventMessageFacilityBase
from .aws_event_message_utility import AwsEventMessageUtility
from app.service.monitoring.logging_service import LoggingService


class AwsEventMessagePublisher(AwsEventMessageFacilityBase):
    _logger = LoggingService()
    
    def __init__(self, aws_region=None):
        super(AwsEventMessagePublisher, self).__init__(aws_region)

    def publish_event(self, event_object):
        try:
            self._logger.info('Start publishing event ...')
            self._logger.info(event_object)

            AwsEventMessageUtility.validate_event_object(event_object)

            topic_name = AwsEventMessageUtility.get_sns_topic_name(type(event_object))
            topic_arn = AwsEventMessageUtility.ensure_sns_topic(self._aws_client.sns, topic_name)
            
            if (not topic_arn):
                self._logger.error('Failed to ensure SNS topic with name: "{0}"'.format(topic_name))
                return

            response = self._aws_client.sns.publish(
                TopicArn=topic_arn,
                Message=event_object.serialize())

            if (not AwsEventMessageUtility.is_success_response(response)):
                self._logger.error('Failed to publish event')
                self._logger.info(response)
            else:
                self._logger.info('Successfully published event')

            return response
        except Exception as e:
            self._logger.error('Failed to publish event: {0}'.format(e))
    