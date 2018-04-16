BenefitMyApp.controller('ConfigureModalController', [
  '$scope', '$modalInstance', 'employeeRecord', 'TimePunchCardSettingsService',
  function($scope, $modalInstance, employeeRecord, TimePunchCardSettingsService){
    $scope.employeeRecord = employeeRecord;

    TimePunchCardSettingsService.GetEmployeeTimeCardSetting(
        employeeRecord.company.id,
        employeeRecord.employee.id)
    .then(
        function(employeeSettingsRecord) {
            $scope.employeeSettingsRecord = employeeSettingsRecord;
        },
        function(errors){
            $modalInstance.close(false);
        });

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.supportAutoReportFullWeek = function() {
        return $scope.employeeSettingsRecord
            && $scope.employeeSettingsRecord.setting
            && $scope.employeeSettingsRecord.setting.autoReportFullWeek;
    };

    $scope.supportAutoReportBreakTime = function() {
        return $scope.employeeSettingsRecord
            && $scope.employeeSettingsRecord.setting
            && $scope.employeeSettingsRecord.setting.autoReportBreakTime;
    };

    $scope.allowReset = function() {
        // Allow reset to company defaults, if this record is persisted
        // with user, and we can delete it to return to the company
        // defaults.
        return $scope.employeeSettingsRecord
            && $scope.employeeSettingsRecord._id;
    };

    $scope.resetToCompanyDefaults = function() {
        // Here, reset to company defaults simply means that we delete the 
        // employee specific settings record, since we rely on the server
        // side service to "flatten" company and user records, the next
        // time we retrieve the settings for the user, we would automatically
        // get the company defaults
        TimePunchCardSettingsService.DeleteEmployeeTimeCardSetting($scope.employeeSettingsRecord)
        .then(
            function() {
                $modalInstance.close(true);
            },
            function(errors) {
                $modalInstance.close(false);
            }
        );
    };

    $scope.save = function() {
        // Save the updates
        TimePunchCardSettingsService.SaveEmployeeTimeCardSetting($scope.employeeSettingsRecord)
        .then(
            function(savedRecord) {
                $modalInstance.close(true);
            },
            function(errors) {
                $modalInstance.close(false);
            }
        );
    };
  }
]).controller('EmployeesTimePunchCardSettingsListController', [
    '$scope',
    '$state',
    '$modal',
    '$controller',
    'CompanyPersonnelsService',
    'utilityService',
    function(
        $scope,
        $state,
        $modal,
        $controller,
        CompanyPersonnelsService,
        utilityService){

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.$watch('company', function(company){
            if(!company){
                return;
            }
            CompanyPersonnelsService.getCompanyEmployees(company.id)
            .then(function(employees){
                // $scope.employeeRecords = employees;
                $scope.employeeRecords = [];
                $scope.employeeRecords.push(
                {
                    "employee": {
                        "first_name": "Alibaba",
                        "last_name": "hahaha"
                    }
                });
                _.each(employees.list, function(employee) {
                    $scope.employeeRecords.push({
                        employee: employee.user,
                        company: company,
                    });
                });
            });
        });

        $scope.configEmployeeSettings = function(employeeRecord) {
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/time_punch_card/modal_edit_settings.html',
                controller: 'ConfigureModalController',
                size: 'md',
                backdrop: 'static',
                resolve: {
                  'employeeRecord': function() {
                    return employeeRecord;
                  }
                }
            });

            modalInstance.result.then(function(success) {
                if (success){
                  var successMessage = "Employee time tracking settings have been updated successfully!";
                  $scope.showMessageWithOkayOnly('Success', successMessage);
                } else{
                  var message = 'Failed to update employee time tracking settings. Please try again later.';
                  $scope.showMessageWithOkayOnly('Error', message);
                }
            });
        };

    }
]).directive('bmEmployeesTimePunchCardSettingsList', function(){

    return {
        restrict: 'E',
        scope: {
          company: '='
        },
        templateUrl: '/static/partials/time_punch_card/directive_employees_time_punch_card_settings_list.html',
        controller: 'EmployeesTimePunchCardSettingsListController'
      };
});
