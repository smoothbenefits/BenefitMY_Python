var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyPersonnelsService',
    ['$q', 'employerWorkerRepository',
    function($q, employerWorkerRepository){
        var initialized = false, personnels = [];

        var _mapEmployeeDomainDataToViewData = function(compRole){
            if (compRole.user.company_group_user.length > 0){
              compRole.company_group_member = compRole.user.company_group_user[0];
            }
            else{
              compRole.company_group_member = {
                company_group:{
                  name:'N/A'
                }
              };
            }
            return compRole;
        };

        var _getCompanyPersonnels = function(companyId){
            return employerWorkerRepository.get({companyId:companyId})
            .$promise.then(function(response){
                var employees = [], brokers = [];
                _.each(response.user_roles, function(role){
                  if(role.company_user_type=='employee')
                  {
                    employees.push(_mapEmployeeDomainDataToViewData(role));
                  }
                  else if(role.company_user_type=='broker')
                  {
                    brokers.push(role);
                  }
                });
                clearCache(companyId);
                var companyPersonnels = {companyId: companyId, brokers: brokers, employees: employees};
                personnels.push(companyPersonnels);
                return companyPersonnels;
            });
        };

        var getCompanyEmployees = function(companyId){
            employeeCollection = _.findWhere(personnels, {companyId: companyId});
            if(!employeeCollection){
                return _getCompanyPersonnels(companyId)
                    .then(function(companyPersonnels){
                        return companyPersonnels.employees;
                    });
            }
            else{
                var deferred = $q.defer();
                deferred.resolve(employeeCollection.employees);
                return deferred.promise;
            }
        };

        var getCompanyBrokers = function(companyId){
            brokerCollection = _.findWhere(personnels, {companyId: companyId});
            if (!brokerCollection){
                return _getCompanyPersonnels(companyId)
                    .then(function(companyPersonnels){
                        return companyPersonnels.brokers;
                    });
            }
            else{
                var deferred = $q.defer();
                deferred.resolve(brokerCollection.brokers);
                return deferred.promise;
            }

        };

        var clearCache = function(compId){
            if(!compId){
                //Remove all the cached data if no company specified
                personnels = [];
            }
            else{
                personnels = _.reject(personnels, function(companyPersonnels){
                    return companyPersonnels.companyId == compId;
                });
            }
        };

        return {
            getCompanyBrokers: getCompanyBrokers,
            getCompanyEmployees: getCompanyEmployees,
            clearCache: clearCache
        };
    }
]);