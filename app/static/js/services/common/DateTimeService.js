var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('DateTimeService',
  ['$q',
   function DateTimeService(
    $q){

        /**
            Get a list of weeks around the current date.
            Params:
                preWeeks - How many weeks to include prior to current week
                postWeeks - How many weeks to include post to the current week
        */
        var GetListOfWeeks = function(preWeeks, postWeeks) {
            var weeks = [];

            // Get the start date of the current week as reference
            var today = moment();
            var startDateOfCurrentWeek = moment(today).startOf('week');

            // Construct the list of weeks and massage the data ready for
            // display
            for (var i = -preWeeks; i <= postWeeks; i++) {
                var weekStartDate = moment(startDateOfCurrentWeek).add(i, 'weeks');
                var weekEndDate = moment(weekStartDate).endOf('week');
                var weekItem = {
                    weekStartDate: weekStartDate,
                    weekEndDate: weekEndDate,
                    weekDisplayText: weekStartDate.format(SHORT_DATE_FORMAT_STRING)
                                    + ' - '
                                    + weekEndDate.format(SHORT_DATE_FORMAT_STRING)
                };

                // Mark the current week for easy selection
                if (weekItem.weekStartDate.isSame(startDateOfCurrentWeek)) {
                    weekItem.isCurrentWeek = true;
                    weekItem.weekDisplayText = weekItem.weekDisplayText + ' [*]'
                }

                weeks.push(weekItem);
            }

            return weeks;
        };

        var GetMonthsInYear = function(){
            var monthsInYear = [];
            var idx = 0;
            while(idx < 12){
                monthsInYear.push({
                    id: idx,
                    name: moment().month(idx).format("MMMM")
                });
                idx++;
            }
            return monthsInYear;
        };

        var GetDaysInMonth = function(){
            var day = 1;
            var daysInMonth = [];
            while(day <= moment().month(0).daysInMonth()){
                daysInMonth.push(day++);
            }
            return daysInMonth
        };

        /**
            Get the begin and end dates of the week that contains 
            the given date.
            @param date expected to be a valid date object
        */
        var GetWeekBoundary = function(date) {
            var startDateOfWeek = moment(date).startOf('week');
            var endDateOfWeek = moment(date).endOf('week');

            return {
                startDateOfWeek: startDateOfWeek,
                endDateOfWeek: endDateOfWeek
            };
        };

        var IsWeekStart = function(date) {
            var startDateOfWeek = moment(date).startOf('week');
            return date.isSame(startDateOfWeek, 'day');
        };

        var IsWeekEnd = function(date) {
            var endDateOfWeek = moment(date).endOf('week');
            return date.isSame(endDateOfWeek, 'day');
        };

        return {
            GetListOfWeeks: GetListOfWeeks,
            GetMonthsInYear: GetMonthsInYear,
            GetDaysInMonth: GetDaysInMonth,
            GetWeekBoundary: GetWeekBoundary,
            IsWeekStart: IsWeekStart,
            IsWeekEnd: IsWeekEnd
        };
    }
]);
