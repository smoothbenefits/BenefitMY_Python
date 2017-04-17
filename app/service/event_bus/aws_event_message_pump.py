import thread
import traceback
import logging
import time
import json

from .aws_event_message_facility_base import AwsEventMessageFacilityBase
from .aws_event_message_utility import AwsEventMessageUtility


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
            self._sns,
            self._sqs,
            event_message_handler_class,
            message_queue_config
        )
        queue_pump.ensure_queue_setup()
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
        def __init__(
            self,
            sns_client,
            sqs_client,
            event_message_handler_class,
            message_queue_config):
            self._sns = sns_client
            self._sqs = sqs_client
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
                self._queue = AwsEventMessageUtility.ensure_sqs_queue(self._sqs, queue_name)
                queue_arn = self._queue.attributes.get('QueueArn')

                # Ensure the SNS topic
                topic_name = AwsEventMessageUtility.get_sns_topic_name(self._message_handler.event_class)
                topic_arn = AwsEventMessageUtility.ensure_sns_topic(self._sns, topic_name)

                # Ensure subscription, queue -> topic
                response = self._sns.subscribe(
                    TopicArn=topic_arn,
                    Protocol='sqs',
                    Endpoint=queue_arn
                )

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

            except Exception as e:
                logging.error(traceback.format_exc())

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
            self._dead_letter_queue = AwsEventMessageUtility.ensure_sqs_queue(self._sqs, dl_queue_name)
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
                logging.error(traceback.format_exc())

        def start_pump_async(self):
            thread.start_new_thread(self._run_pump, ())

        def _run_pump(self):
            while(True):
                self.pump_event_messages()
