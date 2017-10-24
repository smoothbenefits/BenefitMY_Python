import sys
import time
import traceback
import logging
import thread

from django.core.management.base import BaseCommand
from django.conf import settings

from app.service.event_bus.aws_event_bus_service import AwsEventBusService

from app.service.event_bus.event_handlers.environment_test_event_handler import EnvironmentTestEventHandler
from app.service.event_bus.event_handlers.another_environment_test_event_handler import AnotherEnvironmentTestEventHandler
from app.service.event_bus.event_handlers.punch_card_recognition_failed_handler import PunchCardRecognitionFailedHandler
from app.service.event_bus.event_handlers.employee_profile_updated_event_cp_data_sync_handler import EmployeeProfileUpdatedEventCpDataSyncHandler
from app.service.event_bus.event_handlers.person_info_updated_event_cp_data_sync_handler import PersonInfoUpdatedEventCpDataSyncHandler
from app.service.event_bus.event_handlers.w4_updated_event_cp_data_sync_handler import W4UpdatedEventCpDataSyncHandler
from app.service.event_bus.event_handlers.state_tax_updated_event_cp_data_sync_handler import StateTaxUpdatedEventCpDataSyncHandler
from app.service.event_bus.event_handlers.compensation_updated_event_cp_data_sync_handler import CompensationUpdatedEventCpDataSyncHandler
from app.service.event_bus.event_handlers.daily_time_card_audit_report_handler import DailyTimeCardAuditReportHandler
from app.service.event_bus.event_handlers.company_daily_time_card_audit_event_handler import CompanyDailyTimeCardAuditEventHandler

from app.service.event_bus.events.environment_test_event import EnvironmentTestEvent
from app.service.event_bus.aws_message_queue_config import AwsMessageQueueConfig


class Command(BaseCommand):
    def run_process(self):
        # Commenting the below line out, so we do not kick off
        # a ever-running event firing machine by default, but
        # leave it here to help local testing when needed.

        # thread.start_new_thread(self._execute_job, ())
        
        event_bus_service = AwsEventBusService()
        message_pump = event_bus_service.create_event_message_pump()
        
        # Below section constructs needed AWS SQS configurations 
        # that govern behavior of event pumping and handling
        common_sqs_config = AwsMessageQueueConfig()
        common_sqs_config.VisibilityTimeout = 60
        common_sqs_config.MessageRetentionPeriod = 86400
        common_sqs_config.ReceiveMessageWaitTimeSeconds = 20

        # The below section registers all the event handlers
        # Keep appending more registrations for use cases going
        # forward
        message_pump.register_event_message_handler(EnvironmentTestEventHandler, common_sqs_config)
        message_pump.register_event_message_handler(AnotherEnvironmentTestEventHandler, common_sqs_config)
        message_pump.register_event_message_handler(PunchCardRecognitionFailedHandler, common_sqs_config)
        message_pump.register_event_message_handler(EmployeeProfileUpdatedEventCpDataSyncHandler, common_sqs_config)
        message_pump.register_event_message_handler(PersonInfoUpdatedEventCpDataSyncHandler, common_sqs_config)
        message_pump.register_event_message_handler(W4UpdatedEventCpDataSyncHandler, common_sqs_config)
        message_pump.register_event_message_handler(StateTaxUpdatedEventCpDataSyncHandler, common_sqs_config)
        message_pump.register_event_message_handler(CompensationUpdatedEventCpDataSyncHandler, common_sqs_config)
        message_pump.register_event_message_handler(DailyTimeCardAuditReportHandler, common_sqs_config)
        message_pump.register_event_message_handler(CompanyDailyTimeCardAuditEventHandler, common_sqs_config)

        # Now start the pump, which will start pumping and handling
        # with all registered event handlers above
        message_pump.start_pumping(on_new_thread=True)

    def handle(self, *args, **options):
        try:
            self.run_process()
            print 'Worker process running ...'
            while(True):
                pass
        except KeyboardInterrupt:
            print '\nExiting by user request.\n'
            sys.exit(0)
        except:
            pass

    def _execute_job(self):
        try:
            event_bus_service = AwsEventBusService()
            while(1):
                event = EnvironmentTestEvent()
                event_bus_service.publish_event(event)
                time.sleep(10)
        except Exception as e:
            logging.error(traceback.format_exc())

