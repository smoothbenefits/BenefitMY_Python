from .event_base import EventBase


''' 
The event triggered at mid-night every day. i.e. 7am UTC
'''
class Time7AMUTCEvent(EventBase):
    # All time based event is not environment aware and hence
    # subscribes to the same SNS topic that is used across
    # all environments
    # This is because the scheduled timer events are managed
    # out of the app context, and by CloudWatch and AWS Lambda
    # and such, and hence it does not make sense to leak the 
    # set of environments out of the boundary. 
    environment_aware = False

    def __init__(self):
        super(Time7AMUTCEvent, self).__init__()
