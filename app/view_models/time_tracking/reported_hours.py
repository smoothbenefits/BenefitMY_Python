class ReportedHours(object):

    def __init__(self):
        self.paid_hours = 0.0
        self.unpaid_hours = 0.0
        self.overtime_hours = 0.0
        self.paid_time_off_hours = 0.0
        self.sick_time_hours = 0.0

    def get_total_hours(self):
        return self.paid_hours + self.unpaid_hours + self.overtime_hours + \
            self.paid_time_off_hours + self.sick_time_hours
