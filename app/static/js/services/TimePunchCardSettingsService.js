var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimePunchCardSettingsService',
  ['$q',
   'utilityService',
   'TimePunchCardSettingsRepository',
   function TimePunchCardSettingsService(
    $q,
    utilityService,
    TimePunchCardSettingsRepository){

        var GetEmployeeTimeCardSetting = function(companyId, employeeUserId){
            var compDesc = utilityService.getEnvAwareId(companyId);
            var employeeDesc = utilityService.getEnvAwareId(employeeUserId);
            return TimePunchCardSettingsRepository.EmployeeSetting.get(
                {companyDesc: compDesc, personDesc: employeeDesc})
                .$promise.then(function(employeeSetting){
                    return employeeSetting;
                });
        };

        var SaveEmployeeTimeCardSetting = function(settingsModel){
            if (settingsModel._id) {
                // Update
                return TimePunchCardSettingsRepository.EmployeeSettingById.update({id:settingsModel._id}, quotaModel)
                .$promise.then(function(updatedModel){
                    return updatedModel;
                });
            } else {
                // Create
                return TimePunchCardSettingsRepository.EmployeeSettingCollection.save(settingsModel)
                .$promise.then(function(savedModel){
                    return savedModel;
                });
            }
            
        };

        return {
            GetEmployeeTimeCardSetting: GetEmployeeTimeCardSetting,
            SaveEmployeeTimeCardSetting: SaveEmployeeTimeCardSetting
        };
   }
]);