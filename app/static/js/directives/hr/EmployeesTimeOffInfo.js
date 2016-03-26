BenefitMyApp.controller('EmployeesTimeoffInfoController', [
    '$scope',
    'TimeOffService',
    'CompanyPersonnelsService',
    'utilityService',
    function(
        $scope,
        TimeOffService,
        CompanyPersonnelsService,
        utilityService){

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
                        var envAwareId = utilityService.getEnvAwareId(employee.id);
                        var timeoffQuota = _.findWhere(timeoffQuotaList, {personDescriptor: envAwareId});
                        $scope.employeeQuotas.push({
                            employee: employee.user,
                            quota:timeoffQuota
                        });
                    })
                });
            });
            
        });

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