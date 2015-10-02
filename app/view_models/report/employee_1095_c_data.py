class Employee1095CData(object):
    person = ''
    company = ''
    offer_of_coverage = ''
    employee_share = ''
    effective_safe_harbor = ''
    company_safe_harbor = ''
    employee_safe_harbor = ''
    period = ''

    def __init__(self, employee_1095c, company_1095c):

        if (employee_1095c and company_1095c and
            employee_1095c.period != company_1095c.period):
            raise ValueError('The period definitions provided do not match')

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

        self.effective_safe_harbor = self._get_effective_safe_harbor_code(self.employee_safe_harbor,
                                                                     self.company_safe_harbor)

    def _get_effective_safe_harbor_code(self, employee_code, company_code):
        if (employee_code):
            return employee_code
        if (company_code):
            return company_code
        return ''
