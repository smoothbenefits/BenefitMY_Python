from .event_base import EventBase


''' 
The event triggered when a employee's W4 info is updated (including created)
'''
class W4UpdatedEvent(EventBase):
    def __init__(self, user_id=''):
        super(W4UpdatedEvent, self).__init__()
        self.user_id = user_id
