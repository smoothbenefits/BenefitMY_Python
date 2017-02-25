import sys
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from app.service.event_bus.aws_event_bus_service import AwsEventBusService
from app.service.event_bus.events.environment_test_event import EnvironmentTestEvent


class Command(BaseCommand):
    def run_process(self):
        while(1):
            self._execute_job()
            time.sleep(10)

    def handle(self, *args, **options):
        try:
            self.run_process()
        except KeyboardInterrupt:
            print '\nExiting by user request.\n'
            sys.exit(0)
        except:
            pass

    def _execute_job(self):
        print 'Job ran ...'
        event_bus_service = AwsEventBusService()
        event = EnvironmentTestEvent()
        event_bus_service.publish_event(event)
