from .event_base import EventBase


''' 
The event triggered when a employee's compensation is updated (including created)
'''
class CompensationUpdatedEvent(EventBase):
    def __init__(self, user_id=''):
        super(CompensationUpdatedEvent, self).__init__()
        self.user_id = user_id
