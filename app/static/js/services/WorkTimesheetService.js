var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkTimesheetService',
  ['$q',
   'utilityService',
   'WorkTimesheetRepository',
   function WorkTimesheetService(
    $q,
    utilityService,
    WorkTimesheetRepository){

        var _calculateTotalHours = function(weekHours){
            var total = 0;
            _.each(_.values(weekHours), function(hour){
                if(typeof hour === 'number'){
                    total += hour;
                }
            });
            return total;
        };

        var mapDomainModelToViewModel = function(domainModel){
            var viewModel = {
                id: domainModel._id,
                weekStartDate: domainModel.weekStartDate,
                employee: domainModel.employee,
                workHours: domainModel.workHours,
                createdTimestamp: moment(domainModel.createdTimestamp).format(DATE_TIME_FORMAT_STRING),
                updatedTimestamp: moment(domainModel.updatedTimestamp).format(DATE_TIME_FORMAT_STRING),
                totalHours: _calculateTotalHours(domainModel.workHours)
            };
            return viewModel;
        };

        var mapViewModelToDomainModel = function(viewModel) {
          var domainModel = {
            'weekStartDate': viewModel.weekStartDate,
            'workHours': viewModel.workHours,
            'employee': viewModel.employee,
          };

          return domainModel;
        };

        var mapDomainModelListToViewModelList = function(domainModelList){
            var viewModelList = [];
            _.each(domainModelList, function(domainModel){
                viewModelList.push(mapDomainModelToViewModel(domainModel));
            });
            return viewModelList;
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
                'workHours': {
                    'sunday': null,
                    'monday': null,
                    'tuesday': null,
                    'wednesday': null,
                    'thursday': null,
                    'friday': null,
                    'saturday': null
                },
                'updatedTimestamp':'N/A',
                'totalHours': 'N/A'
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
          var dto = mapViewModelToDomainModel(timesheetToSave);
          return WorkTimesheetRepository.Collection.save({}, dto).$promise
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
            GetWorkTimesheetByEmployeeUser: GetWorkTimesheetByEmployeeUser,
            CreateWorkTimesheet: CreateWorkTimesheet,
            UpdateWorkTimesheet: UpdateWorkTimesheet,
            GetWorkTimesheetsByCompany: GetWorkTimesheetsByCompany,
            GetBlankTimesheetForEmployeeUser: GetBlankTimesheetForEmployeeUser
        };
    }
]);
