var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkTimesheetService',
  ['$q',
   'utilityService',
   'WorkTimesheetRepository',
   function WorkTimesheetService(
    $q,
    utilityService,
    WorkTimesheetRepository){

        var BY_STATE_TIMESHEET_TYPE = 'ByState';

        var _calculateTotalHours = function(weekHours){
            var hasAnyValue = false;

            var total = 0;

            if (weekHours) {
                _.each(_.values(weekHours), function(dayHours){
                    if (typeof dayHours.hours === 'number') {
                        hasAnyValue = true;

                        total += dayHours.hours;
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
            return _calculateTotalHours(this.workHours);
        };

        var _calculateTotalOvertimeHours = function() {
            return _calculateTotalHours(this.overtimeHours);
        };

        var GetByStateTag = function(tags) {
          return _.find(tags, function(tag) {
            return tag.tagType === BY_STATE_TIMESHEET_TYPE;
          });
        };

        var mapDomainModelToViewModel = function(domainModel){
            var viewModel = {
                id: domainModel._id,
                _id: domainModel._id,
                weekStartDate: domainModel.weekStartDate,
                employee: domainModel.employee,
                timecards: mapTimecardDomainModelListToViewModelList(domainModel.timecards),
                createdTimestamp: moment(domainModel.createdTimestamp).format(DATE_TIME_FORMAT_STRING),
                updatedTimestamp: moment(domainModel.updatedTimestamp).format(DATE_TIME_FORMAT_STRING)
            };
            return viewModel;
        };

        var mapTimecardDomainToViewModel = function(timecardDomainModel) {
            viewTimeCard = angular.copy(timecardDomainModel);
            stateTag = GetByStateTag(timecardDomainModel.tags);
            if(stateTag){
              viewTimeCard.state = stateTag.tagContent;
            }
            viewTimeCard.getTotalBaseHours = _calculateTotalBaseHours;
            viewTimeCard.getTotalOvertimeHours = _calculateTotalOvertimeHours;
            return viewTimeCard;
        };

        var mapDomainModelListToViewModelList = function(domainModelList){
            var viewModelList = [];
            _.each(domainModelList, function(domainModel){
                viewModelList.push(mapDomainModelToViewModel(domainModel));
            });
            return viewModelList;
        };

        var mapTimecardDomainModelListToViewModelList = function(domainModelList){
            var viewModelList = [];
            _.each(domainModelList, function(domainModel){
                viewModelList.push(mapTimecardDomainToViewModel(domainModel));
            });
            return viewModelList;
        };

        var GetBlankTimecard = function() {
            return {
                tags:[{
                    'tagType': BY_STATE_TIMESHEET_TYPE,
                    'tagContent': ''
                }],
                workHours: getBlankWeekHours(),
                overtimeHours: getBlankWeekHours(),

                getTotalBaseHours: _calculateTotalBaseHours,
                getTotalOvertimeHours: _calculateTotalOvertimeHours
            }
        };

        var getBlankWeekHours = function() {
            return {
                sunday: getBlankDayHours(),
                monday: getBlankDayHours(),
                tuesday: getBlankDayHours(),
                wednesday: getBlankDayHours(),
                thursday: getBlankDayHours(),
                friday: getBlankDayHours(),
                saturday: getBlankDayHours()
            }
        };

        var getBlankDayHours = function() {
            return {
                hours: 0,
                timeRange: {
                    start: null,
                    end: null
                }
            };
        };

        var GetBlankTimesheetForEmployeeUser = function(
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

            var blankViewModel = {
                'weekStartDate': weekStartDateString,
                'employee': employee,
                'timecards': [
                    GetBlankTimecard()
                ]
            };

            return blankViewModel;
        };

        var GetWorkTimesheetByEmployeeUser = function(employeeUser, company, weekStartDate){
            var id = utilityService.getEnvAwareId(employeeUser.id);
            var weekStartDateString = 
                moment(weekStartDate).format(STORAGE_DATE_FORMAT_STRING)

            return WorkTimesheetRepository.ByEmployee.query({
                    userId: id, 
                    start_date: weekStartDateString,
                    end_date: weekStartDateString})
                .$promise.then(function(resultEntries){
                    if (resultEntries && resultEntries.length > 0) {
                        return mapDomainModelToViewModel(resultEntries[0]);
                    } else {
                        return GetBlankTimesheetForEmployeeUser(employeeUser, company, weekStartDateString);
                    }
                });
        };

        var CreateWorkTimesheet = function(timesheetToSave) {
          return WorkTimesheetRepository.Collection.save({}, timesheetToSave).$promise
          .then(function(createdEntry) {
            return createdEntry;
          });
        };

        var UpdateWorkTimesheet = function(timesheetToUpdate){
            return WorkTimesheetRepository.ById.update(
               {id:timesheetToUpdate.id}, 
               timesheetToUpdate)
            .$promise
            .then(function(updatedTimesheet){
                return updatedTimesheet;
            });
        }

        var GetWorkTimesheetsByCompany = function(companyId, weekStartDate){
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
            BY_STATE_TIMESHEET_TYPE: BY_STATE_TIMESHEET_TYPE,
            GetBlankTimecard: GetBlankTimecard,
            GetByStateTag: GetByStateTag,
            GetWorkTimesheetByEmployeeUser: GetWorkTimesheetByEmployeeUser,
            CreateWorkTimesheet: CreateWorkTimesheet,
            UpdateWorkTimesheet: UpdateWorkTimesheet,
            GetWorkTimesheetsByCompany: GetWorkTimesheetsByCompany,
            GetBlankTimesheetForEmployeeUser: GetBlankTimesheetForEmployeeUser
        };
    }
]);
