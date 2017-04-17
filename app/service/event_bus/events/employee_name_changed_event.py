from .event_base import EventBase


''' A Test event designed to test the running environment
    of the worker is proper based on settings
'''
class EmployeeNameChangedEvent(EventBase):
    def __init__(self, original_value=None, updated_value=None):
        super(EmployeeNameChangedEvent, self).__init__()
        self.original_value = original_value
        self.updated_value = updated_value
