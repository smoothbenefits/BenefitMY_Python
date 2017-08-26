from .event_base import EventBase


''' 
The event triggered when a person info is updated (including created)
'''
class PersonInfoUpdatedEvent(EventBase):
    def __init__(self, person_id=''):
        super(PersonInfoUpdatedEvent, self).__init__()
        self.person_id = person_id
