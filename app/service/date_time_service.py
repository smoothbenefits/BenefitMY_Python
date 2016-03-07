from datetime import timedelta


class DateTimeService(object):

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
