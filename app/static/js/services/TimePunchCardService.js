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
                'adminOnly': true
            },
        };

        var sanitizeViewModel = function(punchCard) {
            if (!this.timeRangeOn) {
                punchCard.start = null;
                punchCard.end = null;
            }
        };

        var PunchCardTypeBehaviors = {
            'WorkTime': {
                'timeRangeOn': true,
                'includedInTotalHours': true,
                'sanitizeViewModel': sanitizeViewModel
            },
            'PartialDayOff': {
                'timeRangeOn': true,
                'includedInTotalHours': true,
                'sanitizeViewModel': sanitizeViewModel
            },
            'FullDayOff': {
                'timeRangeOn': false,
                'includedInTotalHours': false,
                'sanitizeViewModel': sanitizeViewModel
            }
        };

        var PunchCardTypes = {
            'WorkTime': {
                'name': 'Work Time',
                'behavior': PunchCardTypeBehaviors.WorkTime
            },
            'CompanyHoliday': {
                'name': 'Company Holiday',
                'behavior': PunchCardTypeBehaviors.FullDayOff
            },
            'PaidTimeOff': {
                'name': 'Paid Time Off',
                'behavior': PunchCardTypeBehaviors.PartialDayOff
            },
            'SickTime': {
                'name': 'Sick Time',
                'behavior': PunchCardTypeBehaviors.PartialDayOff
            },
            'PersonalLeave': {
                'name': 'Personal Leave',
                'behavior': PunchCardTypeBehaviors.PartialDayOff
            }
        };

        // Transform the card types to an array and cache for continued
        // uses.
        var punchCardTypesArray = $.map(PunchCardTypes, function(value, index) {
                return [value];
            });

        var GetAvailablePunchCardTypes = function() {
            return punchCardTypesArray;
        };

        // Global default start and end time for new cards
        var defaultStartTime = new Date();
        defaultStartTime.setHours(0);
        defaultStartTime.setMinutes(0);

        var defaultEndTime = new Date();
        defaultEndTime.setHours(0);
        defaultEndTime.setMinutes(0);

        var mapDomainToViewModel = function(domainModel) {
            var viewModel = angular.copy(domainModel);

            // Map out the card attributes for front-end usage
            viewModel.attributes = mapAttributesDomainToViewModel(domainModel.attributes);


            // Map out the card type to one of the object defined in
            // PunchCardTypes above
            viewModel.recordType = _.find(punchCardTypesArray, function(cardType) {
                return cardType.name == domainModel.recordType;
            });

            // Attach utility functions
            viewModel.getTimeRangeDisplayText = function() {
                if (!this.start || !this.end) {
                    return 'N/A';
                }

                return moment(this.start).format('HH:mm')
                    + ' - '
                    + moment(this.end).format('HH:mm');
            };

            viewModel.getDuration = function(){
                if (!this.start || !this.end) {
                    return 0;
                }
                var startTime = moment(this.start);
                var endTime = moment(this.end);

                // Get time difference between start and end time in hour before rounding
                return endTime.diff(startTime, 'hours', true);
            };

            return viewModel;
        };

        var mapViewToDomainModel = function(viewModel) {
            var domainModel = angular.copy(viewModel);

            // Map out the card attributes for storage
            domainModel.attributes = mapAttributesViewToDomainModel(viewModel.attributes);

            // Map out the card type name
            domainModel.recordType = viewModel.recordType.name;

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
                    id: null,
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
                                result.project.id = domainAttr.value;
                                ProjectService.GetProjectById(domainAttr.value)
                                    .then(function(project){
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

        var GetBlankPunchCardForEmployeeUser = function(
            employeeUser,
            companyId,
            date) {
            var employee = {
                'personDescriptor': utilityService.getEnvAwareId(employeeUser.id),
                'firstName': employeeUser.first_name,
                'lastName': employeeUser.last_name,
                'email': employeeUser.email,
                'companyDescriptor': utilityService.getEnvAwareId(companyId)
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

        var GetPunchCards = function(repoEndpoint, apiId, startDate, endDate){
            var id = utilityService.getEnvAwareId(apiId);

            return repoEndpoint.query({
                id: id,
                start_date: startDate,
                end_date: endDate
            }).$promise.then(function(punchCards){
                var resultCards = [];
                if (punchCards && punchCards.length > 0) {
                    _.each(punchCards, function(domainModel) {
                        resultCards.push(mapDomainToViewModel(domainModel));
                    });
                }
                return resultCards;
            });
        }

        var GetWeeklyPunchCardsByEmployeeUser = function(employeeUser, weekStartDate, weekEndDate){
            var weekStartDateString = moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING);
            var weekEndDateString = moment(weekEndDate).format(STORAGE_DATE_FORMAT_STRING);

            return GetPunchCards(
                TimePunchCardRepository.ByEmployee,
                employeeUser.id,
                weekStartDateString,
                weekEndDateString).then(function(punchCards){
                    return MapPunchCardsToWeekdays(punchCards);
                });
        };

        var GetAllPunchCardsByCompany = function(companyId){
            return GetPunchCards(
                TimePunchCardRepository.ByCompany,
                companyId,
                undefined,
                undefined).then(function(punchCards){
                    var groupedPunchCards = _.groupBy(punchCards, function(card) {
                      return card.employee.personDescriptor;
                    });
                    return groupedPunchCards;
                });
        };

        var GetPunchCardsByCompanyTimeRange = function(companyId, weekStartDate){
            weekStartDateString = moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING);
            weekEndDateString = moment(weekStartDate).add(7, 'days').format(STORAGE_DATE_FORMAT_STRING);
            return GetPunchCards(
                TimePunchCardRepository.ByCompany,
                companyId,
                weekStartDateString,
                weekEndDateString).then(function(punchCards){
                    var groupedPunchCards = _.groupBy(punchCards, function(card) {
                      return card.employee.personDescriptor;
                    });
                    return groupedPunchCards;
                });
        };

        var FilteredCardsForTotalHours = function(punchCards){
          if (!punchCards || punchCards.length <= 0){
            return [];
          }
            // Get record types of which punch cards should be included in calculation
          var includedRecordTypes = _.filter(PunchCardTypes, function(type) {
            return type.behavior.includedInTotalHours;
          });

          var includedRecordTypeNames = _.map(includedRecordTypes, function(type) {
            return type.name;
          });

          return _.filter(punchCards, function(card) {
            var cardType = card.recordType ? card.recordType.name : '';
            return _.contains(includedRecordTypeNames, cardType);
          });
        }

        var CalculateTotalHours = function(punchCards) {

          var includedPunchCards = FilteredCardsForTotalHours(punchCards);

          // Calculate total time for each employee
          // Set initial reduce value to 0
          var totalTimeInHour = _.reduce(includedPunchCards, function(memo, punchCard) {
            return memo + punchCard.getDuration();
          }, 0);

          return totalTimeInHour;
        };

        var OrderPunchCardsByTime = function(punchCards) {
            return _.sortBy(punchCards, function(card) {
                return card.start;
            });
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
          CalculateTotalHours: CalculateTotalHours,
          GetWeeklyPunchCardsByEmployeeUser: GetWeeklyPunchCardsByEmployeeUser,
          GetPunchCardsByCompanyTimeRange: GetPunchCardsByCompanyTimeRange,
          GetAllPunchCardsByCompany: GetAllPunchCardsByCompany,
          GetBlankPunchCardForEmployeeUser: GetBlankPunchCardForEmployeeUser,
          FilteredCardsForTotalHours: FilteredCardsForTotalHours
        };
    }
]);
