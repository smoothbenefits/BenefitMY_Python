BenefitMyApp.controller('ConfigureModalController', [
  '$scope', '$modalInstance', 'employeeQuota', 'TimeOffService',
  function($scope, $modalInstance, employeeQuota, TimeOffService){
    $scope.timeoffQuota = employeeQuota.quota;

    if (!$scope.timeoffQuota) {
        $scope.timeoffQuota = TimeOffService.GetBlankTimeOffQuota(
                employeeQuota.company.id,
                employeeQuota.employee.id);
    }

    $scope.accrualFrequencyTypes = TimeOffService.GetAvailableAccrualFrequecy();

    $scope.cancel = function() {
        $modalInstance.dismiss();
    };

    $scope.save = function() {
        TimeOffService.UpdateTimeOffQuotaByUser(
            employeeQuota.employee.id,
            $scope.timeoffQuota);
        $modalInstance.close(true);
    };
  }
]).controller('EmployeesTimeoffInfoController', [
    '$scope',
    '$state',
    '$modal',
    '$controller',
    'TimeOffService',
    'CompanyPersonnelsService',
    'utilityService',
    function(
        $scope,
        $state,
        $modal,
        $controller,
        TimeOffService,
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
                TimeOffService.GetTimeOffQuotaByCompany(
                    $scope.company.id)
                .then(function(timeoffQuotaList){
                    $scope.employeeQuotas = [];
                    _.each(employees, function(employee){
                        var envAwareId = utilityService.getEnvAwareId(employee.user.id);
                        var timeoffQuota = _.findWhere(timeoffQuotaList, {personDescriptor: envAwareId});
                        $scope.employeeQuotas.push({
                            employee: employee.user,
                            company: company,
                            quota: timeoffQuota
                        });
                    })
                });
            });
        });

        $scope.configEmployeeAccrualSpecs = function(employeeQuota) {
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/timeoff/modal_edit_accrual_specs.html',
                controller: 'ConfigureModalController',
                size: 'md',
                backdrop: 'static',
                resolve: {
                  'employeeQuota': function() {
                    return employeeQuota;
                  }
                }
            });

            modalInstance.result.then(function(success){
                if (success){
                  var successMessage = "Configuration of employee time off has been saved successfully!";
                  $scope.showMessageWithOkayOnly('Success', successMessage);
                } else{
                  var message = 'Failed to save employee time off configuration. Please try again later.';
                  $scope.showMessageWithOkayOnly('Error', message);
                }

                $state.reload();
            });
        };

    }
]).directive('bmEmployeesTimeOffInfo', function(){

    return {
        restrict: 'E',
        scope: {
          company: '='
        },
        templateUrl: '/static/partials/timeoff/directive_employees_time_off_info.html',
        controller: 'EmployeesTimeoffInfoController'
      };
});
