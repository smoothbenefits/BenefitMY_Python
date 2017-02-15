var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyPersonnelsService',
    ['$q', 'employerWorkerRepository', 'EmployeeProfileService',
    function($q, employerWorkerRepository, EmployeeProfileService){
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

        var _GetPaginatedEmployees = function(employeeList, pageNum, pageSize){
            var totalCount = employeeList.length;
            var pagedList = employeeList;
            var offset = 0;
            var offsetEnd = pageSize * pageNum;
            var totalPages = Math.ceil(totalCount/pageSize);

            if(pageNum > totalPages){
                pageNum = totalPages;
            }
            offset = (pageNum - 1) * pageSize;
            offsetEnd = pageNum * pageSize;
            if(offsetEnd > totalCount){
                offsetEnd = totalCount;
            }
            pagedList = employeeList.slice(offset, offsetEnd);

            return {
                totalCount: totalCount,
                list: pagedList,
            };
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

        var GetPaginatedEmployees = function(companyId, pageNum, pageSize, status, filterProfileId){

            return $q.all([
                    getCompanyEmployees(companyId),
                    EmployeeProfileService.initializeCompanyEmployees(companyId)
                ]).then(function(values){
                    var employees = values[0];
                    var profiles = values[1];
                    _.each(employees, function(employee){
                        var foundProfile = _.find(profiles, function(profile){
                            return profile.person.user == employee.user.id;
                        });
                        employee.profile = foundProfile;
                    });
                    var filteredEmployees = _.filter(employees, function(employee){
                      return employee.profile && 
                        employee.profile.employment_status == status && 
                        (!filterProfileId || employee.profile.id == filterProfileId);
                    });
                    
                    return _GetPaginatedEmployees(
                        _.sortBy(filteredEmployees, function(emp){
                            return emp.user.last_name;
                        }),
                        pageNum,
                        pageSize);
                });
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
            clearCache: clearCache,
            GetPaginatedEmployees: GetPaginatedEmployees
        };
    }
]);
