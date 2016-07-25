from datetime import timedelta
from datetime import date
import dateutil.parser


class DateTimeService(object):

    TIME_UNIT_PRECISION = 1

    def get_last_week_range_by_date(self, date):
        curr_week_range = self.get_week_range_by_date(date)
        return (
            curr_week_range[0] - timedelta(7),
            curr_week_range[1] - timedelta(7))

    def get_week_range_by_date(self, date):
        """Find the first/last day of the week for the given day.
        Assuming weeks start on Sunday and end on Saturday.

        Returns a tuple of ``(start_date, end_date)``.

        """
        # isocalendar calculates the year, week of the year, and day
        # of the week.
        # dow is Mon = 1, Sat = 6, Sun = 7
        year, week, dow = date.isocalendar()

        # Find the first day of the week.
        if dow == 7:
            # Since we want to start with Sunday, let's test for that
            # condition.
            start_date = date
        else:
            # Otherwise, subtract `dow` number days to get the first day
            start_date = date - timedelta(dow)

        # Now, add 6 for the last day of the week (i.e., count up to Saturday)
        end_date = start_date + timedelta(6)

        return (start_date, end_date)

    def get_list_of_week_start_dates_in_range(self, start_date, end_date):
        """
            Get the list of week start dates that fall in the given date 
            range
        """
        week_list = []    

        week_delta = timedelta(7)
        start_week_range = self.get_week_range_by_date(start_date)
        start_week_begin = start_week_range[0]
        end_week_range = self.get_week_range_by_date(end_date)
        end_week_end = end_week_range[1]

        curr_week_begin = start_week_begin

        while curr_week_begin <= end_week_end:
            week_list.append(curr_week_begin)
            curr_week_begin += week_delta 

        return week_list

    def parse_date_time(self, date_time_string):
        return dateutil.parser.parse(date_time_string)

    def get_time_diff_in_hours(self, start_time, end_time):
        delta = end_time - start_time
        return round(delta.total_seconds() / 3600, self.TIME_UNIT_PRECISION)
