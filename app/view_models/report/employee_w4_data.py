class EmployeeW4Data(object):

    def __init__(self, employee_w4):
        self.total_points = ''
        self.extra_amount = ''
        self.marriage_status = ''

        if (employee_w4):
            self.total_points = employee_w4.user_defined_points
            if (self.total_points is None):
                self.total_points = employee_w4.calculated_points
            
            self.extra_amount = 0
            if (employee_w4.extra_amount):
                self.extra_amount = employee_w4.extra_amount

            self.marriage_status = employee_w4.marriage
