from .event_base import EventBase


''' 
The event solely created for testing purposes. No event handlers
rolled outside of test/development environment is ok to hook
to this event.
'''
class TestGlobalEvent(EventBase):
    # This is a global test event, and hence does not multiplex
    # for specific environments
    environment_aware = False

    def __init__(self):
        super(TestGlobalEvent, self).__init__()
