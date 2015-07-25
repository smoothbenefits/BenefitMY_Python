var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('employeeBenefitElectionService',
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
              if(!existEmployee.selectedBenefits){
                existEmployee.selectedBenefits = [];
              }
              existEmployee.selectedBenefits.push(benefitSelectionItem);
            }
          });
        };

        var addWaivedToEmployeeList = function(waviedList){
          _.each(waviedList, function(waivedItem){
            var existEmployee = _.find(employeeList, function(employee){
              return employee.user.id === waivedItem.userId;
            });
            if (existEmployee){
              if(!existEmployee.waivedList){
                existEmployee.waivedList = [];
              }
              existEmployee.waivedList.push(waivedItem);
            }
          });
        }

        employerWorkerRepository.get({companyId: companyId})
        .$promise.then(function(users){
          _.each(users.user_roles, function(compUser){
            if(compUser.company_user_type === 'employee'){
              compUser.name = compUser.user.last_name;
              employeeList.push(compUser);
            }
          });

          BenefitElectionService.getBenefitElectionsByCompany(companyId)
          .then(function(array){
            addBenefitPlanToSelectionList(array);
            _.each(employeeList, function(employee){
                if(!employee.selectedBenefits){
                  employee.selectedBenefits = [];
                  employee.selectedBenefits.push({selectedPlanName:'No Selection', lastUpdatedTime:'N/A', enrolled:[{name:'N/A'}]});
                }
              });
            BenefitElectionService.getBenefitWaivedListByCompany(companyId)
            .then(function(waivedList){
              addWaivedToEmployeeList(waivedList);
              deferred.resolve(employeeList);
            }, function(errorResponse){
              deferred.reject(errorResponse);
            });
          }, function(errorResponse){
            deferred.reject(errorResponse);
          });

        });

        return deferred.promise;
    };
}]);
