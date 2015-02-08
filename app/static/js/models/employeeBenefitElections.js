var benefitmyModels = angular.module('benefitmyModels', ['benefitmyService']);


benefitmyModels.factory('employeeBenefitElections',
    ['BenefitElectionService',
     'employerWorkerRepository',
     '$q',
  function(BenefitElectionService, employerWorkerRepository, $q){
    return function(companyId){
        var deferred = $q.defer();
        var employeeList = [];

        var addBenefitPlanToSelectionList = function(benefitSelectionArray){
          _.each(benefitSelectionArray, function(benefitSelectionItem){
            var existEmployee = _.find(employeeList, function(employee){
              return employee.user.id === benefitSelectionItem.userId;
            });
            if (existEmployee){
              if(!existEmployee.benefits){
                existEmployee.benefits = [];
              }
              existEmployee.benefits.push(benefitSelectionItem);
              existEmployee.updated = benefitSelectionItem.lastUpdatedTime;
              if(!existEmployee.waivedList){
                existEmployee.waivedList = [];
              }
              if(benefitSelectionItem.waivedList && benefitSelectionItem.updated){
                existEmployee.waivedList = benefitSelectionItem.waivedList;
                existEmployee.updated = benefitSelectionItem.updated;
              }
            }
          });
        };

        employerWorkerRepository.get({companyId: companyId})
        .$promise.then(function(users){
          _.each(users.user_roles, function(compUser){
            if(compUser.company_user_type === 'employee'){
              compUser.name = compUser.user.last_name;
              employeeList.push(compUser);
            }
          });
          
          BenefitElectionService.getBenefitElectionsByCompany(companyId, function(array){
            addBenefitPlanToSelectionList(array);
             _.each(employeeList, function(employee){
                if(!employee.benefits){
                  employee.updated = 'N/A';
                  employee.benefits = [];
                  employee.benefits.push({selectedPlanName:'No Selection', lastUpdatedTime:'N/A', enrolled:[{name:'N/A'}]});
                }
                if(!employee.waivedList){
                  employee.waivedList = [];
                  employee.waivedList.push('N/A');
                }
              });
             deferred.resolve(employeeList);
          }, function(errorResponse){
            deferred.reject(errorResponse);
          });

        });

        return deferred.promise;
    };
}]);


