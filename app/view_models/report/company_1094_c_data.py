class Company1094CMonthlyData(object):

    def __init__(self, monthly_info, period):

        if monthly_info:
            self.is_empty = False
            self.company = monthly_info.company
            self.minimum_essential_coverage = monthly_info.minimum_essential_coverage
            self.fulltime_employee_count = monthly_info.fulltime_employee_count
            self.total_employee_count = monthly_info.total_employee_count
            self.aggregated_group = monthly_info.aggregated_group
            self.section_4980h_transition_relief = monthly_info.section_4980h_transition_relief
            self.period = monthly_info.period
        else:
            self.is_empty = True
            self.period = period

class Company1094CData(object):

    def __init__(self, member_info, monthly_info, periods):

        if member_info:
            self.company = member_info.company
            self.number_of_1095c = member_info.number_of_1095c
            self.authoritative_transmittal = member_info.authoritative_transmittal
            self.member_of_aggregated_group = member_info.member_of_aggregated_group
            self.certifications_of_eligibility = member_info.certifications_of_eligibility
        else:
            self.number_of_1095c = 0
            self.authoritative_transmittal = False
            self.member_of_aggregated_group = False
            self.certifications_of_eligibility = ''

        self.monthly_info = []
        for period in periods:
            if not period:
                continue
            
            monthly_data = next((datum for datum in monthly_info if datum.period == period), None)
            monthly_view_model = Company1094CMonthlyData(monthly_data, period)
            self.monthly_info.append(monthly_view_model)
