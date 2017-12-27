from .event_base import EventBase


''' 
The event to report (email) employee data changes on the system
to appropriate audiences 
'''
class CompanyDailyEmployeeDataChangeReportEvent(EventBase):

    def __init__(self, company_id=''):
        super(CompanyDailyEmployeeDataChangeReportEvent, self).__init__()
        self.company_id = company_id
