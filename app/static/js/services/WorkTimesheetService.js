var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkTimesheetService',
  ['$q',
   'utilityService',
   'WorkTimesheetRepository',
   function WorkTimesheetService(
    $q,
    utilityService,
    WorkTimesheetRepository){
        var mapDomainModelToViewModel = function(domainModel){
            var viewModel = {
                id: domainModel._id,
                weekStartDate: domainModel.weekStartDate,
                employee: domainModel.employee,
                workHours: domainModel.workHours,
                createdTimestamp: moment(domainModel.createdTimestamp).format(DATE_TIME_FORMAT_STRING),
                updatedTimestamp: moment(domainModel.updatedTimestamp).format(DATE_TIME_FORMAT_STRING)
            };
            return viewModel;
        };

        var mapViewModelToDomainModel = function(viewModel) {
          var domainModel = {
            'weekStartDate': viewModel.weekStartDate,
            'workHours': viewModel.workHours,
            'employee': viewModel.employee
          };

          return domainModel;
        };

        var getBlankTimesheetForEmployeeUser = function(employeeUser, weekStartDateString) {
            // First convert employee user struct to employee data required by the DTO
            var employee = {
                'personDescriptor': utilityService.getEnvAwareId(employeeUser.id),
                'firstName': employeeUser.first_name,
                'lastName': employeeUser.last_name,
                'email': employeeUser.email
            };

            var blankViewModel = {
                'weekStartDate': weekStartDateString,
                'employee': employee,
                'workHours': {
                    'sunday': null,
                    'monday': null,
                    'tuesday': null,
                    'wednesday': null,
                    'thursday': null,
                    'friday': null,
                    'saturday': null
                }
            };

            return blankViewModel;
        };

        var GetWorkTimesheetByEmployeeUser = function(employeeUser, weekStartDate){
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
                        return getBlankTimesheetForEmployeeUser(employeeUser, weekStartDateString);
                    }
                });
        };

        var CreateWorkTimesheet = function(timesheetToSave) {
          var dto = mapViewModelToDomainModel(timesheetToSave);
          return WorkTimesheetRepository.Collection.save({}, dto).$promise
          .then(function(createdEntry) {
            return createdEntry;
          });
        };

        return {
            GetWorkTimesheetByEmployeeUser: GetWorkTimesheetByEmployeeUser,
            CreateWorkTimesheet: CreateWorkTimesheet
        };
    }
]);
