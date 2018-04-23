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
                return TimePunchCardSettingsRepository.EmployeeSettingById.update({id:settingsModel._id}, settingsModel)
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

        var DeleteEmployeeTimeCardSetting = function(settingsModel){
            if (settingsModel._id) {
                return TimePunchCardSettingsRepository.EmployeeSettingById.delete({id:settingsModel._id}).$promise;
            } 
        };

        var GetAllEmployeesTimeCardSetting = function(companyId) {
            var compDesc = utilityService.getEnvAwareId(companyId);
            return TimePunchCardSettingsRepository.AllEmployeeSettings.get(
                {companyDesc: compDesc})
                .$promise.then(function(allEmployeesSetting){
                    return allEmployeesSetting;
                });
        };

        return {
            GetEmployeeTimeCardSetting: GetEmployeeTimeCardSetting,
            SaveEmployeeTimeCardSetting: SaveEmployeeTimeCardSetting,
            DeleteEmployeeTimeCardSetting: DeleteEmployeeTimeCardSetting,
            GetAllEmployeesTimeCardSetting: GetAllEmployeesTimeCardSetting
        };
   }
]);