from .event_base import EventBase


''' 
The event triggered when an employee's profile is updated (including created)
'''
class EmployeeProfileUpdatedEvent(EventBase):
    def __init__(self, company_id='', user_id=''):
        super(EmployeeProfileUpdatedEvent, self).__init__()
        self.company_id = company_id
        self.user_id = user_id
