import json
from datetime import datetime


class EventHandlerBase(object):
    def __init__(self, event_class):
        ''' Requires to register the target class of
            the event this is handling
        ''' 
        self.event_class = event_class

    ''' Handle the event.
        Note: the event here an instance of the event_class
              registered for this handler.
    ''' 
    def handle(self, event):
        raise NotImplementedError()
