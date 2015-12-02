class Employee1095CData(object):

    def __init__(self, employee_1095c):
        self.company = ''
        self.period = ''
        self.offer_of_coverage = ''
        self.employee_share = ''
        self.safe_harbor = ''
        
        if employee_1095c:
            if hasattr(employee_1095c, 'person'):
                self.person = employee_1095c.person

            self.company = employee_1095c.company
            self.period = employee_1095c.period
            self.offer_of_coverage = employee_1095c.offer_of_coverage
            self.employee_share = employee_1095c.employee_share
            self.safe_harbor = employee_1095c.safe_harbor
