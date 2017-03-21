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


        var _filterEmployeeListByProfileId = function(profileId){
            var filtered = _.filter(this.list, function(employee){
                return employee.profile && employee.profile.id == profileId;
            });
            this.list = filtered;
            return this;
        };

        var _filterEmployeeListByTimeRangeStatus = function(
            requiredOnStatus,
            requiredOnExcludeStatus,
            timeRangeStart,
            timeRangeEnd)
        {
            var filtered = _.filter(this.list, function(employee) {
                if (!timeRangeStart || !timeRangeEnd) {
                    // If time range is not provided, 
                    // assume start and to be now, so this becomes 
                    // a check against the current status
                    timeRangeStart = timeRangeEnd = moment();
                }

                var activeStatues = employee.profile.getListOfEmploymentStatusInTimeRange(timeRangeStart, timeRangeEnd);

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
            });
            this.list = filtered;
            return this;
        };

        var _searchByName = function(term){
            return _.filter(this.list, function(employee){
                var fullName = employee.profile.first_name + ' ' + employee.profile.last_name;
                return fullName.toLowerCase().indexOf(term.toLowerCase()) > -1;
            });
        };

        var _getPaginated = function(pageNum, pageSize){
            var totalCount = this.list.length;
            var pagedList = this.list;
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
            pagedList = this.list.slice(offset, offsetEnd);

            return {
                totalCount: totalCount,
                list: pagedList,
            };
        };

        var _constructEmployeeListWithProfile = function(employeeList, companyId){
            var deferred = $q.defer();

            EmployeeProfileService.getCompanyEmployeeProfiles(companyId)
            .then(function(employeeProfiles) {
                _.each(employeeList, function(employee){
                    var foundProfile = _.find(employeeProfiles, function(profile){
                        return profile.person.user == employee.user.id;
                    });
                    employee.profile = foundProfile;
                });
                var employeeListBuilder = {
                    list: employeeList,
                    filterByProfileId: _filterEmployeeListByProfileId,
                    filterByTimeRangeStatus: _filterEmployeeListByTimeRangeStatus,
                    search: _searchByName,
                    paginate: _getPaginated
                }
                deferred.resolve(employeeListBuilder);
            });

            return deferred.promise;
        };

        var getCompanyEmployees = function(companyId){
            employeeCollection = _.findWhere(personnels, {companyId: companyId});
            if(!employeeCollection){
                return _getCompanyPersonnels(companyId)
                    .then(function(companyPersonnels){
                        return companyPersonnels.employees;
                    })
                    .then(function(allEmployees) {
                        return _constructEmployeeListWithProfile(
                            allEmployees,
                            companyId
                        );
                    });
            }
            else {
                return _constructEmployeeListWithProfile(
                    employeeCollection.employees,
                    companyId
                );
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
