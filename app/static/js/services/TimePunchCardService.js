var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimePunchCardService',
  ['$q',
   'utilityService',
   function TimePunchCardService(
    $q,
    utilityService){

        var AttributeTypes = {
            'State': 'state',
            'Project': 'project'
        };

        var PunchCardTypes = {
            'WorkDay': 'Work Day',
            'NotWorkDay': 'Not a Work Day',
            'CompanyHoliday': 'Company Holiday',
            'PaidTimeOff': 'Paid Time Off',
            'SickTime': 'Sick Time',
            'PersonalLeave': 'Personal Leave'
        };

        var GetAvailablePunchCardTypes = function() {
            var result = $.map(PunchCardTypes, function(value, index) {
                return [value];
            });

            return result;
        };

        /**
         ###################################
         # Begin Mock Data Section 
         ###################################
        */

        var existingCards = [
            {
              'employee': null, // Not needed for mockup
              'date': new Date(2016, 6, 1),
              'start': new Date(2016, 6, 1, 9, 0, 0),
              'end': new Date(2016, 6, 1, 15, 0, 0),
              'recordType': PunchCardTypes.WorkDay,
              'attributes': []
            },
            {
              'employee': null, // Not needed for mockup
              'date': new Date(2016, 6, 1),
              'start': new Date(2016, 6, 1, 15, 0, 0),
              'end': new Date(2016, 6, 1, 18, 0, 0),
              'recordType': PunchCardTypes.PaidTimeOff,
              'attributes': []
            },
            {
              'employee': null, // Not needed for mockup
              'date': new Date(2016, 6, 2),
              'start': new Date(2016, 6, 2, 8, 0, 0),
              'end': new Date(2016, 6, 2, 14, 0, 0),
              'recordType': PunchCardTypes.WorkDay,
              'attributes': [
                {
                    'name': AttributeTypes.Project,
                    'value': 'ABC Building'
                }
              ]
            },
            {
              'employee': null, // Not needed for mockup
              'date': new Date(2016, 6, 2),
              'start': new Date(2016, 6, 2, 14, 0, 0),
              'end': new Date(2016, 6, 2, 18, 0, 0),
              'recordType': PunchCardTypes.WorkDay,
              'attributes': [
                {
                    'name': AttributeTypes.State,
                    'value': 'Florida'
                }
              ]
            },
            {
              'employee': null, // Not needed for mockup
              'date': new Date(2016, 6, 3),
              'start': new Date(2016, 6, 3, 8, 0, 0),
              'end': new Date(2016, 6, 3, 18, 0, 0),
              'recordType': PunchCardTypes.PersonalLeave,
              'attributes': []
            }
        ];

        /**
         ###################################
         # End Mock Data Section 
         ###################################
        */

        var defaultStartTime = new Date();
        defaultStartTime.setHours(0);
        defaultStartTime.setMinutes(0);

        var defaultEndTime = new Date();
        defaultEndTime.setHours(0);
        defaultEndTime.setMinutes(0);

        var GetBlankPunchCardForEmployeeUser = function(
            employeeUser,
            company,
            date) {
            var employee = {
                'personDescriptor': utilityService.getEnvAwareId(employeeUser.id),
                'firstName': employeeUser.first_name,
                'lastName': employeeUser.last_name,
                'email': employeeUser.email,
                'companyDescriptor': utilityService.getEnvAwareId(company.id)
            };
            return {
              'employee': employee,
              'date': date,
              'start': defaultStartTime,
              'end': defaultEndTime,
              'attributes': []
            }; 
        }

        var CreatePunchCard = function(punchCardToSave) {
            existingCards.push(punchCardToSave);
        };

        var UpdatePunchCard = function(punchCardToUpdate) {
        };

        var DeletePunchCard = function(punchCardToDelete) {
            existingCards = _.without(existingCards, punchCardToDelete);
        };

        var GetWeeklyPunchCardsByEmployeeUser = function(employeeUser, company, weekStartDate){
            var allCards = existingCards;
            return MapPunchCardsToWeekdays(allCards, weekStartDate);
        };

        var GetWeeklyPunchCardsByCompany = function(companyId, weekStartDate){
            var allCards = existingCards;
            return MapPunchCardsToWeekdays(allCards, weekStartDate);
        };

        var FilterPunchCardsByWeek = function(punchCards, weekStartDate) {
            return punchCards; 
        };

        var OrderPunchCardsByTime = function(punchCards) {
            return punchCards
        };

        var MapPunchCardsToWeekdays = function(punchCards, weekStartDate) {
            var cardsInWeek = FilterPunchCardsByWeek(punchCards, weekStartDate);
            var cardsInWeekOrdered = OrderPunchCardsByTime(cardsInWeek);
            return _.groupBy(cardsInWeekOrdered, function(card) {
                return card.date.getDay();
            });
        };

        return {
          GetAvailablePunchCardTypes: GetAvailablePunchCardTypes,
          GetWeeklyPunchCardsByEmployeeUser: GetWeeklyPunchCardsByEmployeeUser,
          CreatePunchCard: CreatePunchCard,
          UpdatePunchCard: UpdatePunchCard,
          DeletePunchCard: DeletePunchCard,
          GetWeeklyPunchCardsByCompany: GetWeeklyPunchCardsByCompany,
          GetBlankPunchCardForEmployeeUser: GetBlankPunchCardForEmployeeUser
        };
    }
]);
