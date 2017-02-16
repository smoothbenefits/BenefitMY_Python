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

        var _filterEmployeeListByEmploymentStatus = function(employeeList, companyId, employeeStatusFilterSpecs) {
            var deferred = $q.defer();

            // Filter specs not specified, just return original list
            if (!employeeStatusFilterSpecs) {
                deferred.resolve(employeeList);
            }

            EmployeeProfileService.initializeCompanyEmployees(companyId)
            .then(function(employeeProfiles) {
                _.each(employeeList, function(employee){
                    var foundProfile = _.find(employeeProfiles, function(profile){
                        return profile.person.user == employee.user.id;
                    });
                    employee.profile = foundProfile;
                });
                var filteredEmployees = _.filter(employeeList, function(employee){
                  return employee.profile && employeeStatusFilterSpecs.profileMatches(employee.profile);
                });
                deferred.resolve(filteredEmployees);
            });

            return deferred.promise;
        };

        var getCompanyEmployees = function(
            companyId,
            employeeStatusFilterSpecs){
            employeeCollection = _.findWhere(personnels, {companyId: companyId});
            if(!employeeCollection){
                return _getCompanyPersonnels(companyId)
                    .then(function(companyPersonnels){
                        return companyPersonnels.employees;
                    })
                    .then(function(allEmployees) {
                        return _filterEmployeeListByEmploymentStatus(
                            allEmployees,
                            companyId,
                            employeeStatusFilterSpecs
                        );
                    });
            }
            else {
                return _filterEmployeeListByEmploymentStatus(
                    employeeCollection.employees,
                    companyId,
                    employeeStatusFilterSpecs
                );
            }
        };

        var GetPaginatedEmployees = function(companyId, pageNum, pageSize, status){
            var filterSpecs = constructEmployeeStatusFilterSpecs(status);
            return getCompanyEmployees(companyId, filterSpecs).then(function(filteredEmployees) {
                return _GetPaginatedEmployees(
                    _.sortBy(filteredEmployees, function(emp) {
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

        var constructEmployeeStatusFilterSpecs = function(
            requiredOnStatus,
            requiredOnExcludeStatus,
            timeRangeStart,
            timeRangeEnd) {

            return {
                requiredOnStatus: requiredOnStatus,
                timeRangeStart: timeRangeStart,
                timeRangeEnd: timeRangeEnd,

                profileMatches: function(employeeProfile) {
                    if (!timeRangeStart || !timeRangeEnd) {
                        // If time range is not provided, 
                        // assume start and to be now, so this becomes 
                        // a check against the current status
                        timeRangeStart = timeRangeEnd = moment();
                    }

                    var activeStatues = employeeProfile.getListOfEmploymentStatusInTimeRange(timeRangeStart, timeRangeEnd);

                    // First check that required-on status is active in the range
                    if (requiredOnStatus && !_.contains(activeStatues, requiredOnStatus)) {
                        return false;
                    }

                    // Then check that if exclude status is specified, there are 
                    // indeed some statuses that are on during the range, beside
                    // the excluded status.
                    // One common need for this is to answer "is the employee at
                    // least partially employed during the time period" 
                    if (requiredOnExcludeStatus && !_.some(activeStatues, function(status) {
                        return status != requiredOnExcludeStatus;
                    })) {
                        return false;
                    }

                    return true;
                }
            };
        };

        return {
            getCompanyBrokers: getCompanyBrokers,
            getCompanyEmployees: getCompanyEmployees,
            clearCache: clearCache,
            GetPaginatedEmployees: GetPaginatedEmployees,
            constructEmployeeStatusFilterSpecs: constructEmployeeStatusFilterSpecs
        };
    }
]);
