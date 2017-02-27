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

    def register_event_message_handler(self, event_message_handler_class):
        queue_pump = self.AwsQueuePump(
            self._sns,
            self._sqs,
            event_message_handler_class
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
            event_message_handler_class):
            self._sns = sns_client
            self._sqs = sqs_client
            self._event_message_handler_class = event_message_handler_class
            self._queue = None

        def ensure_queue_setup(self):
            try:
                # Validate the handler class
                instance = self._event_message_handler_class()
                AwsEventMessageUtility.validate_event_handler_instance(instance)

                # Ensure setup of the message queue
                queue_name = AwsEventMessageUtility.get_sqs_queue_name(instance)
                self._queue = AwsEventMessageUtility.ensure_sqs_queue(self._sqs, queue_name)
                queue_arn = self._queue.attributes.get('QueueArn')

                # Ensure the SNS topic
                topic_name = AwsEventMessageUtility.get_sns_topic_name(instance.event_class)
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
        
            except Exception as e:
                logging.error(traceback.format_exc())

        def pump_event_messages(self):
            try:
                messages = self._queue.receive_messages()

                # Process messages
                for message in messages:

                    # Print out the body and author (if set)
                    print message
                    print message.body

                    # Let the queue know that the message is processed
                    message.delete()
            except Exception as e:
                logging.error(traceback.format_exc())

        def start_pump_async(self):
            thread.start_new_thread(self._run_pump, ())

        def _run_pump(self):
            while(True):
                self.pump_event_messages()
