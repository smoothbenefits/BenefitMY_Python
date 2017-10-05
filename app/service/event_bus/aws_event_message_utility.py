import boto3

from django.conf import settings
from .events.event_base import EventBase
from .event_handlers.event_handler_base import EventHandlerBase


class AwsEventMessageUtility(object):

    ################################
    ## Constants
    ################################

    # Policy statement to allow SNS to forward to SQS queues
    queue_policy_statement = {
        "Sid": "auto-transcode",
        "Effect": "Allow",
        "Principal": {
            "AWS": "*"
        },
        "Action": "SQS:SendMessage",
        "Resource": "<SQS QUEUE ARN>",
        "Condition": {
            "StringLike": {
                "aws:SourceArn": "<SNS TOPIC ARN>"
            }
        }
    }

    ################################
    ## SNS Handling
    ################################

    @staticmethod
    def validate_event_object(event_object):
        if (not isinstance(event_object, EventBase)):
            raise Exception('The given object is not of the event type!')

    @staticmethod
    def get_sns_topic_name(event_class):
        class_name = event_class.__name__
        if (event_class.environment_aware):
            return settings.ENVIRONMENT_IDENTIFIER + '_' + class_name
        else:
            return class_name

    @staticmethod
    def ensure_sns_topic(sns_client, topic_name):
        response = sns_client.create_topic(Name=topic_name)
        if (not AwsEventMessageUtility.is_success_response(response)):
            return None
        return response['TopicArn']

    ################################
    ## SQS Handling
    ################################
    
    @staticmethod
    def validate_event_handler_instance(event_handler_instance):
        if (not isinstance(event_handler_instance, EventHandlerBase)):
            raise Exception('The given instance is not a event handler!')

    @staticmethod
    def get_sqs_queue_name(event_message_handler_instance):
        handler_class_name = type(event_message_handler_instance).__name__
        event_class_name = event_message_handler_instance.event_class.__name__
        # If the event class name is repeated in the handler name, remove it
        # This is an attempt to reduce the length of the queue name
        # So to reduce the chance of it being over the limit
        handler_class_name = handler_class_name.replace(event_class_name, '')
        plain_name = settings.ENVIRONMENT_IDENTIFIER + '_' + event_class_name + '_' + handler_class_name

        if (len(plain_name) > 80):
            raise Exception('The queue name is too long per SQS specification: {0}'.format(plain_name))

        return plain_name

    @staticmethod
    def ensure_sqs_queue(sqs_client, queue_name, delay_seconds=5):
        return sqs_client.create_queue(QueueName=queue_name, Attributes={'DelaySeconds': str(delay_seconds)})

    ################################
    ## Common 
    ################################

    @staticmethod
    def is_success_response(aws_client_response):
        return aws_client_response['ResponseMetadata']['HTTPStatusCode'] < 400
