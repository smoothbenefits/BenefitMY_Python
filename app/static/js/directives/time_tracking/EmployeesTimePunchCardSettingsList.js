BenefitMyApp.controller('ConfigureModalController', [
  '$scope', '$modalInstance', 'employeeRecord',
  function($scope, $modalInstance, employeeRecord){
    $scope.employeeRecord = employeeRecord;

    if (!$scope.employeeRecord) {
        // Get blank record
    }

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        // Save the updates
        $modalInstance.close(true);
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

            modalInstance.result.then(function(success){
                if (success){
                  var successMessage = "Employee time tracking settings have been saved successfully!";
                  $scope.showMessageWithOkayOnly('Success', successMessage);
                } else{
                  var message = 'Failed to save employee time tracking settings. Please try again later.';
                  $scope.showMessageWithOkayOnly('Error', message);
                }

                $state.reload();
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
