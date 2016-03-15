var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkTimePunchCardService',
  ['$q',
   'utilityService',
   'WorkTimesheetRepository',
   function WorkTimePunchCardService(
    $q,
    utilityService,
    WorkTimesheetRepository){

        var BY_STATE_PUNCHCARD_TYPE = 'ByState';

        var _calculateTotalHours = function(timecards){
          var hasAnyValue = false;
          var total = 0;

          if (timecards) {
            _.each(timecards, function(timecard) {
              var workHours = timecard.workHours;
              if (weekHours) {
                _.each(_.values(weekHours), function(hourObj){
                  if(typeof hourObj.hours === 'number'){
                    hasAnyValue = true;
                    total += hourObj.hours;
                  }
                });
              }
            });
          }

          // If there is not any valid number in the week hours,
          // simply set to 'N/A' for display
          if (!hasAnyValue) {
            total = 'N/A'
          }
          else{
            total = total.toFixed(1);
          }

          return total;
        };

        var _calculateTotalBaseHours = function() {
            return _calculateTotalHours(this.timecards);
        };

        var mapDomainModelToViewModel = function(domainModel){
            var viewModel = {
                id: domainModel._id,
                weekStartDate: domainModel.weekStartDate,
                employee: domainModel.employee,
                timecards: domainModel.timecards,
                overtimeHours: domainModel.overtimeHours,
                createdTimestamp: moment(domainModel.createdTimestamp).format(DATE_TIME_FORMAT_STRING),
                updatedTimestamp: moment(domainModel.updatedTimestamp).format(DATE_TIME_FORMAT_STRING),
                getTotalBaseHours: _calculateTotalBaseHours
            };
            return viewModel;
        };

        var mapViewModelToDomainModel = function(viewModel) {
          var domainModel = {
            'weekStartDate': viewModel.weekStartDate,
            'timecards': viewModel.timecards,
            'employee': viewModel.employee
          };

          _.each(domainModel.timecards, function(timecard) {
            var workHours = timecard.workHours;
            var keys = _.keys(workHours);
            // Calculate total hours base on start and end time
            _.each(keys, function(key) {
              var notApplicable = workHours[key].notApplicable;
              if (notApplicable) {
                // If the day does not have reported hours, set hours to 0
                // and start/end time to the beginning of the epoch
                workHours[key].hours = 0;
                workHours[key].start = new Date(0);
                workHours[key].end = new Date(0);
              } else {
                var start = workHours[key].timeRange.start;
                var end = workHours[key].timeRange.end;
                // Substrction provide difference in milliseconds.
                // Convert to hours and assigned to field
                workHours[key].hours = Math.abs(start - end) / 36e5;
              }
            });
          });

          return domainModel;
        };

        var mapDomainModelListToViewModelList = function(domainModelList){
            var viewModelList = [];
            _.each(domainModelList, function(domainModel){
                viewModelList.push(mapDomainModelToViewModel(domainModel));
            });
            return viewModelList;
        };

        var getByStateTag = function(tags) {
          return _.find(tags, function(tag) {
            return tag.tagType === BY_STATE_PUNCHCARD_TYPE;
          });
        };

        var GetWorkHoursByState = function(punchCard) {
          var workHoursByStateList = [];
          if (punchCard && punchCard.timecards) {
            _.each(punchCard.timecards, function(timecard) {
              var stateTag = getByStateTag(timecard.tags);
              var transposed = {state: stateTag.tagContent};
              var keys = _.keys(timecard.workHours);
              _.each(keys, function(key) {
                //Do single decimal rounding
                transposed[key] = Math.round(timecard.workHours[key].hours * 10) / 10;
              });
              workHoursByStateList.push(transposed);
            });
          }

          return workHoursByStateList;
        };

        var GetBlankPunchCardForEmployeeUser = function(
            employeeUser,
            company,
            weekStartDateString) {
            // First convert employee user struct to employee data required by the DTO
            var employee = {
                'personDescriptor': utilityService.getEnvAwareId(employeeUser.id),
                'firstName': employeeUser.first_name,
                'lastName': employeeUser.last_name,
                'email': employeeUser.email,
                'companyDescriptor': utilityService.getEnvAwareId(company.id)
            };

            var defaultStartTime = new Date();
            defaultStartTime.setHours(8);
            defaultStartTime.setMinutes(0);

            var defaultEndTime = new Date();
            defaultEndTime.setHours(18);
            defaultEndTime.setMinutes(0);

            var blankViewModel = {
                'weekStartDate': weekStartDateString,
                'employee': employee,
                'timecards': [{
                  'workHours': {
                    'sunday': {
                      'notApplicable': true,
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'monday': {
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'tuesday': {
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'wednesday': {
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'thursday': {
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'friday': {
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    },
                    'saturday': {
                      'notApplicable': true,
                      'hours': null,
                      'timeRange': {
                        'start': defaultStartTime,
                        'end': defaultEndTime
                      }
                    }
                  },
                  'tags': [{
                    'tagType': BY_STATE_PUNCHCARD_TYPE,
                    'tagContent': ''
                  }]
                }],
                getTotalBaseHours: _calculateTotalBaseHours,
                'updatedTimestamp':'N/A'
            };

            return blankViewModel;
        };

        var GetWorkPunchCardByEmployeeUser = function(employeeUser, company, weekStartDate){
          var id = utilityService.getEnvAwareId(employeeUser.id);
          var weekStartDateString = moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING);

          return WorkTimesheetRepository.ByEmployee.query({
                  userId: id,
                  start_date: weekStartDateString,
                  end_date: weekStartDateString})
              .$promise.then(function(resultEntries){
                  if (resultEntries && resultEntries.length > 0) {
                      return mapDomainModelToViewModel(resultEntries[0]);
                  } else {
                      return GetBlankPunchCardForEmployeeUser(employeeUser, company, weekStartDateString);
                  }
              });
        };

        var CreateWorkPunchCard = function(punchCardToSave) {
          var dto = mapViewModelToDomainModel(punchCardToSave);
          return WorkTimesheetRepository.Collection.save({}, dto).$promise
          .then(function(createdEntry) {
            return createdEntry;
          });
        };

        var UpdateWorkPunchCard = function(punchCardToUpdate){
            return WorkTimesheetRepository.ById.update(
               {id:punchCardToUpdate.id},
               punchCardToUpdate)
            .$promise
            .then(function(updatedEntry){
                return updatedEntry;
            });
        };

        var GetWorkPunchCardsByCompany = function(companyId, weekStartDate){
            var weekStartDateString =
                moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING);
            var compId = utilityService.getEnvAwareId(companyId)
            return WorkTimesheetRepository.ByCompany.query({
                    companyId: compId,
                    start_date: weekStartDateString,
                    end_date: weekStartDateString
                })
                .$promise.then(function(workSheets){
                    return mapDomainModelListToViewModelList(workSheets);
                });
        };

        return {
          BY_STATE_PUNCHCARD_TYPE: BY_STATE_PUNCHCARD_TYPE,
          GetWorkHoursByState: GetWorkHoursByState,
          GetWorkPunchCardByEmployeeUser: GetWorkPunchCardByEmployeeUser,
          CreateWorkPunchCard: CreateWorkPunchCard,
          UpdateWorkPunchCard: UpdateWorkPunchCard,
          GetWorkPunchCardsByCompany: GetWorkPunchCardsByCompany,
          GetBlankPunchCardForEmployeeUser: GetBlankPunchCardForEmployeeUser
        };
    }
]);
