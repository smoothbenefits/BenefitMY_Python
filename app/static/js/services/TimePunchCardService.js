var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimePunchCardService',
  ['$q',
   'utilityService',
   'ProjectService',
   'TimePunchCardRepository',
   function TimePunchCardService(
    $q,
    utilityService,
    ProjectService,
    TimePunchCardRepository){

        // Define supported attributes on time punch cards
        // 'name' - is the attribute name expected to get persisted
        // 'displayText' - is the text used for displaying the attributes on UI
        // 'adminOnly' - determines whether only admin has view/edit rights to the attribute
        var AttributeTypes = {
            'State': {
                'name': 'State',
                'displayText': 'State',
                'adminOnly': false
            },
            'Project': {
                'name': 'Project',
                'displayText': 'Project',
                'adminOnly': false
            },
            'HourlyRate': {
                'name': 'HourlyRate',
                'displayText': 'Hourly Rate',
                'adminOnly': false
            },
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
            viewModel.attributes = mapAttributesDomainToViewModel(domainModel.attributes);
            
            return viewModel;
        };

        var mapViewToDomainModel = function(viewModel) {
            var domainModel = angular.copy(viewModel);
            domainModel.attributes = mapAttributesViewToDomainModel(viewModel.attributes);

            // Delete this to avoid mongo db error 
            delete domainModel._id

            return domainModel;
        };

        var mapAttributesDomainToViewModel = function(attributesDomainModel) {
            // Domain model of attributes is expected to be an array
            // Where view model of attributes we define it to be an object
            //  holding attributes we care as properties
            var result = {
                'state': {
                    type: AttributeTypes.State,
                    value: null
                },
                'project': {
                    type: AttributeTypes.Project,
                    value: null
                },
                'hourlyRate': {
                    type: AttributeTypes.HourlyRate,
                    value: null
                }
            };

            if (attributesDomainModel && attributesDomainModel.length > 0) {
                for (i = 0; i < attributesDomainModel.length; i++) {
                    var domainAttr = attributesDomainModel[i];
                    if (domainAttr.value) {
                        switch(domainAttr.name) {
                            case AttributeTypes.State.name:
                                result.state.value = domainAttr.value;
                                break;
                            case AttributeTypes.Project.name:
                                // TODO:
                                // Needs to translate to project object via
                                // Project Service. This requires building
                                // a cache for this access first.
                                ProjectService.GetProjectById(domainAttr.value).then(function(project) {
                                    result.project.value = project;
                                });
                                break;
                            case AttributeTypes.HourlyRate.name:
                                result.hourlyRate.value = Number(domainAttr.value).toFixed(2); 
                                break;
                            default:
                                break;
                        }
                    }
                }
            }
            
            return result; 
        };

        var mapAttributesViewToDomainModel = function(attributesViewModel) {
            // Domain model of attributes is expected to be an array
            // Where view model of attributes we define it to be an object
            //  holding attributes we care as properties
            var result = [];

            if (attributesViewModel) {
                if (attributesViewModel.state && attributesViewModel.state.value) {
                    result.push({
                        'name': AttributeTypes.State.name,
                        'value': attributesViewModel.state.value
                    });
                } 

                if (attributesViewModel.project && attributesViewModel.project.value) {
                    result.push({
                        'name': AttributeTypes.Project.name,
                        'value': attributesViewModel.project.value._id
                    });
                } 

                if (attributesViewModel.hourlyRate && attributesViewModel.hourlyRate.value) {
                    result.push({
                        'name': AttributeTypes.HourlyRate.name,
                        'value': attributesViewModel.hourlyRate.value
                    });
                }
            } 
            
            return result;
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
