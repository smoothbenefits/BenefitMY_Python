class ReportedHours(object):

    def __init__(self):
        self.paid_hours = 0.0
        self.unpaid_hours = 0.0

    def get_total_hours(self):
        return self.paid_hours + self.unpaid_hours
