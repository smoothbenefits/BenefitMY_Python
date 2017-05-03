class EmployeePinService(object):

    def get_company_wide_unique_pin(self, company_id, user_id):
        return '{0:04d}'.format(user_id)
