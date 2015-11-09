class Employee1095CData(object):

    def __init__(self, employee_1095c, company_1095c):
        if (employee_1095c and company_1095c and
            employee_1095c.period != company_1095c.period):
            raise ValueError('The period definitions provided do not match')

        self.company = ''
        self.offer_of_coverage = ''
        self.employee_share = ''
        self.company_safe_harbor = ''
        self.employee_safe_harbor = ''
        self.period = ''
        self.person = ''
        self.effective_safe_harbor = ''

        if (company_1095c):
            self.company = company_1095c.company
            self.offer_of_coverage = company_1095c.offer_of_coverage
            self.employee_share = company_1095c.employee_share
            self.company_safe_harbor = company_1095c.safe_harbor
            self.period = company_1095c.period

        if (employee_1095c):
            self.person = employee_1095c.person
            self.company = employee_1095c.company
            self.period = employee_1095c.period
            self.employee_safe_harbor = employee_1095c.safe_harbor

        self.effective_safe_harbor = self._get_effective_safe_harbor_code()

    def _get_effective_safe_harbor_code(self):
        if hasattr(self, 'employee_safe_harbor') and self.employee_safe_harbor:
            return self.employee_safe_harbor
        if hasattr(self, 'company_safe_harbor') and self.company_safe_harbor:
            return self.company_safe_harbor
        return ''
