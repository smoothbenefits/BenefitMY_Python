from django.conf import settings

from .event_base import EventBase


''' A Test event designed to test the running environment
    of the worker is proper based on settings
'''
class EnvironmentTestEvent(EventBase):
    def __init__(self):
        super(EnvironmentTestEvent, self).__init__()
        self.environment = settings.ENVIRONMENT_IDENTIFIER
        self.host_url = settings.SITE_URL
