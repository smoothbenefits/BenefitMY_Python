from .event_base import EventBase


''' 
The event triggered when a employee's State tax info is updated (including created)
'''
class StateTaxUpdatedEvent(EventBase):
    def __init__(self, user_id='', state=''):
        super(StateTaxUpdatedEvent, self).__init__()
        self.user_id = user_id
        self.state = state
