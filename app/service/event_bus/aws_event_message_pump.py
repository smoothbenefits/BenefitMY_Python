import thread
import traceback
import time
import json

from .aws_event_message_facility_base import AwsEventMessageFacilityBase
from .aws_event_message_utility import AwsEventMessageUtility
from app.service.monitoring.logging_service import LoggingService


class AwsEventMessagePump(AwsEventMessageFacilityBase):

    def __init__(self, aws_region=None):
        super(AwsEventMessagePump, self).__init__(aws_region)
        
        # Collection of per-queue pumps
        self._queue_pumps = []

    def register_event_message_handler(
        self,
        event_message_handler_class,
        message_queue_config=None):
        queue_pump = self.AwsQueuePump(
            self._aws_client,
            event_message_handler_class,
            message_queue_config
        )
        success = queue_pump.ensure_queue_setup()

        if (success):
            self._queue_pumps.append(queue_pump)

    def start_pumping(self, on_new_thread=False):
        if (on_new_thread):
            thread.start_new_thread(self._run_queue_pumps_async, ())
        else:
            self._run_queue_pumps_sync()

    def _run_queue_pumps_sync(self):
        while(True):
            for queue_pump in self._queue_pumps:
                queue_pump.pump_event_messages()
            time.sleep(10)

    def _run_queue_pumps_async(self):
        for queue_pump in self._queue_pumps:
            queue_pump.start_pump_async()


    ''' Nested class to help encapsulating the logic bound to
        per-queue based message handling
    '''
    class AwsQueuePump(object):
        _logger = LoggingService()
        
        def __init__(
            self,
            aws_client,
            event_message_handler_class,
            message_queue_config):
            self._aws_client = aws_client
            self._event_message_handler_class = event_message_handler_class
            self._queue = None
            self._dead_letter_queue = None
            self._message_handler = None
            self._message_queue_config = message_queue_config

        def ensure_queue_setup(self):
            try:
                # Validate the handler class
                self._message_handler = self._event_message_handler_class()
                AwsEventMessageUtility.validate_event_handler_instance(self._message_handler)

                # Ensure setup of the message queue
                queue_name = AwsEventMessageUtility.get_sqs_queue_name(self._message_handler)
                self._queue = AwsEventMessageUtility.ensure_sqs_queue(self._aws_client.sqs, queue_name)
                
                if (not self._queue):
                    self._logger.error('Failed to ensure event message queue with name: "{0}"'.format(queue_name))
                    return False
                queue_arn = self._queue.attributes.get('QueueArn')

                # Ensure the SNS topic
                topic_name = AwsEventMessageUtility.get_sns_topic_name(self._message_handler.event_class)
                topic_arn = AwsEventMessageUtility.ensure_sns_topic(self._aws_client.sns, topic_name)

                if (not topic_arn):
                    self._logger.error('Failed to ensure SNS topic with name: "{0}"'.format(topic_name))
                    return False

                # Ensure subscription, queue -> topic
                response = self._aws_client.sns.subscribe(
                    TopicArn=topic_arn,
                    Protocol='sqs',
                    Endpoint=queue_arn
                )

                if (not AwsEventMessageUtility.is_success_response(response)):
                    self._logger.error('Failed to ensure SQS-SNS subscription: "{0}-{1}"'.format(queue_name, topic_name))
                    return False

                # Set up a policy to allow SNS access to the queue
                if 'Policy' in self._queue.attributes:
                    policy = json.loads(self._queue.attributes['Policy'])
                else:
                    policy = {'Version': '2008-10-17'}

                if 'Statement' not in policy:
                    statement = AwsEventMessageUtility.queue_policy_statement
                    statement['Resource'] = queue_arn
                    statement['Condition']['StringLike']['aws:SourceArn'] = topic_arn
                    policy['Statement'] = [statement]

                    self._queue.set_attributes(Attributes={
                        'Policy': json.dumps(policy)
                    })

                # Now setup the queue config if specified
                if (self._message_queue_config):
                    self._queue.set_attributes(Attributes=self._message_queue_config.to_dict())
                
                # Now ensure the setup of the dead-letter queue
                self._ensure_dead_letter_queue(queue_name)

                return True

            except Exception as e:
                self._logger.error(traceback.format_exc())

        ''' This is to ensure the proper setup of dead-letter
            queue.
            For now, this is not yet made highly configurable
            from the consumer side, and below is the hardcoded
            setup:
                * Source queue is 1-1 mapped to a corresponding dead-letter queue
                * The queue configuration for all dead-letter queues use SQS defaults
                * Redrive policy on the source queue is set to allow max 5 recerives
                  of a message before moving it to dead-letter queue

            All of these knobs could be later on exposed on API for consumers
            to control/override, but this is not a priority for now.
        '''
        def _ensure_dead_letter_queue(self, source_queue_name):
            dl_queue_name = source_queue_name + '_DL'
            self._dead_letter_queue = AwsEventMessageUtility.ensure_sqs_queue(self._aws_client.sqs, dl_queue_name)
            
            if (not self._dead_letter_queue):
                self._logger.error('Failed to ensure deadletter queue for: "{0}"'.format(source_queue_name))
                return

            dl_queue_arn = self._dead_letter_queue.attributes.get('QueueArn')
            redrive_policy = {
                'maxReceiveCount': '5',
                'deadLetterTargetArn': dl_queue_arn
            }
            self._queue.set_attributes(Attributes={
                'RedrivePolicy': json.dumps(redrive_policy)
            })

        def pump_event_messages(self):
            try:
                messages = self._queue.receive_messages()

                # Process messages
                for message in messages:
                    self._logger.info('Handling event message: {0}'.format(message.body))

                    # Parse out the actual event message from 
                    # Boto3 sqs message data structure
                    # And deserialize into the expected event 
                    # instance.
                    body = json.loads(message.body)
                    event_message = body.get('Message', '{}')
                    event_instance = self._message_handler.event_class()
                    event_instance.deserialize(event_message)

                    # Delegate to the message handler to handle
                    self._message_handler.handle(event_instance)

                    # Let the queue know that the message is processed
                    message.delete()
            except Exception as e:
                self._logger.error(traceback.format_exc())

        def start_pump_async(self):
            thread.start_new_thread(self._run_pump, ())

        def _run_pump(self):
            while(True):
                self.pump_event_messages()
