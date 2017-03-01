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
from app.service.event_bus.events.environment_test_event import EnvironmentTestEvent


class Command(BaseCommand):
    def run_process(self):
        thread.start_new_thread(self._execute_job, ())
        
        event_bus_service = AwsEventBusService()
        message_pump = event_bus_service.create_event_message_pump()
        message_pump.register_event_message_handler(EnvironmentTestEventHandler)
        message_pump.register_event_message_handler(AnotherEnvironmentTestEventHandler)
        message_pump.start_pumping(on_new_thread=True)

    def handle(self, *args, **options):
        try:
            self.run_process()
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
