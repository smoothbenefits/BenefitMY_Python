var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimePunchCardService',
  ['$q',
   'utilityService',
   'TimePunchCardRepository',
   function TimePunchCardService(
    $q,
    utilityService,
    TimePunchCardRepository){

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

        var mapDomainToViewModel = function(domainModel) {
            var viewModel = angular.copy(domainModel);
            return viewModel;
        };

        var mapViewToDomainModel = function(viewModel) {
            var domainModel = angular.copy(viewModel);

            // Delete this to avoid mongo db error 
            delete domainModel._id

            return domainModel;
        };

        // Global default start and end time for new cards
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
            var domainModel = {
              'employee': employee,
              'date': date,
              'start': defaultStartTime,
              'end': defaultEndTime,
              'attributes': []
            };

            return mapDomainToViewModel(domainModel); 
        };

        var CreatePunchCard = function(punchCardToSave) {
          var domainModel = mapViewToDomainModel(punchCardToSave);
          return TimePunchCardRepository.Collection.save({}, domainModel).$promise
          .then(function(createdEntry) {
            return mapDomainToViewModel(createdEntry);
          });
        };

        var UpdatePunchCard = function(punchCardToUpdate) {
            var domainModel = mapViewToDomainModel(punchCardToUpdate);
            return TimePunchCardRepository.ById.update(
               {id:punchCardToUpdate._id},
               domainModel)
            .$promise
            .then(function(updatedEntry){
                return mapDomainToViewModel(updatedEntry);
            });
        };

        var SavePunchCard = function(punchCardToSave) {
            if (punchCardToSave._id) {
                return UpdatePunchCard(punchCardToSave);
            } else {
                return CreatePunchCard(punchCardToSave);
            }
        };

        var DeletePunchCard = function(punchCardToDelete) {
            return TimePunchCardRepository.ById.delete(
               {id:punchCardToDelete._id})
            .$promise
            .then(function(response){
                return response;
            });
        };

        var GetWeeklyPunchCardsByEmployeeUser = function(employeeUser, weekStartDate, weekEndDate){
            var id = utilityService.getEnvAwareId(employeeUser.id);
            var weekStartDateString = moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING);
            var weekEndDateString = moment(weekEndDate).format(STORAGE_DATE_FORMAT_STRING);

            return TimePunchCardRepository.ByEmployee.query({
                  userId: id,
                  start_date: weekStartDateString,
                  end_date: weekEndDateString})
              .$promise.then(function(punchCards) {
                var resultCards = [];
                if (punchCards && punchCards.length > 0) {
                    _.each(punchCards, function(domainModel) {
                        resultCards.push(mapDomainToViewModel(domainModel));
                    });
                }
                return MapPunchCardsToWeekdays(resultCards);
              });
        };

        var GetWeeklyPunchCardsByCompany = function(companyId, weekStartDate, weekEndDate){
            var allCardsInWeek = existingCards;
            return MapPunchCardsToWeekdays(allCardsInWeek);
        };

        var OrderPunchCardsByTime = function(punchCards) {
            return punchCards;
        };

        var MapPunchCardsToWeekdays = function(punchCards) {
            var cardsInWeekOrdered = OrderPunchCardsByTime(punchCards);
            return _.groupBy(cardsInWeekOrdered, function(card) {
                var date = new Date(card.date)
                return date.getDay();
            });
        };

        return {
          GetAvailablePunchCardTypes: GetAvailablePunchCardTypes,
          SavePunchCard: SavePunchCard,
          DeletePunchCard: DeletePunchCard,
          GetWeeklyPunchCardsByEmployeeUser: GetWeeklyPunchCardsByEmployeeUser,
          GetWeeklyPunchCardsByCompany: GetWeeklyPunchCardsByCompany,
          GetBlankPunchCardForEmployeeUser: GetBlankPunchCardForEmployeeUser
        };
    }
]);
