import json
from datetime import datetime


class EventHandlerBase(object):
    def __init__(self, event_class):
        ''' Requires to register the target class of
            the event this is handling
        ''' 
        self.event_class = event_class

    def handle(self, event_message):
        raise NotImplementedError()
