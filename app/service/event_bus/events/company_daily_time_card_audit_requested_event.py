from .event_base import EventBase


''' 
The event to represent that a daily audit for a company's 
time card is requested
'''
class CompanyDailyTimeCardAuditEvent(EventBase):

    def __init__(self, company_id=''):
        super(CompanyDailyTimeCardAuditEvent, self).__init__()
        self.company_id = company_id
