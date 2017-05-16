from django.conf import settings

from .event_base import EventBase


''' 
The event triggered when time punch card photo recognition is below the confidance threshold
'''
class PunchCardRecognitionFailedEvent(EventBase):
    def __init__(self):
        super(PunchCardRecognitionFailedEvent, self).__init__()
        self.environment = settings.ENVIRONMENT_IDENTIFIER
        self.host_url = settings.SITE_URL
        self.company_id = ''
        self.user_id = ''
        self.in_progress = False
        self.photo_url = ''
        self.created = None
