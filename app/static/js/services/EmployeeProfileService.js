var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployeeProfileService',
    ['$q',
    'EmployeeProfileRepository',
    'EmployeeManagementEmployeeTerminationRepository',
    'PersonService',
    function (
        $q,
        EmployeeProfileRepository,
        EmployeeManagementEmployeeTerminationRepository,
        PersonService){
        var isFullTimeEmploymentType = function(employeeProfile) {
          if (!employeeProfile) {
            return false;
          }
          return employeeProfile.employmentType === 'FullTime';
        };

        var _cachedEmployeeProfiles = [];

        var mapDomainToViewModel = function(employeeProfileDomainModel) {
            var viewModel = {};

            viewModel.id = employeeProfileDomainModel.id;
            viewModel.jobTitle = employeeProfileDomainModel.job_title;
            viewModel.employmentType = employeeProfileDomainModel.employment_type;
            viewModel.employmentStatus = employeeProfileDomainModel.employment_status;
            viewModel.personId = employeeProfileDomainModel.person;
            viewModel.companyId = employeeProfileDomainModel.company;
            viewModel.lastUpdateDateTime = moment(employeeProfileDomainModel.updated_at).format(DATE_FORMAT_STRING);
            viewModel.employeeNumber = employeeProfileDomainModel.employee_number;
            viewModel.manager = employeeProfileDomainModel.manager;

            if (employeeProfileDomainModel.department && employeeProfileDomainModel.department.department) {
                viewModel.department = employeeProfileDomainModel.department.department;
            } else {
                viewModel.department = "";
            }

            // TODO:
            // The below logic is quite cumbersome, but just to get the view model
            // working with angular's "date" input type...
            // Since the initialization of Date counts in the effect of time zone,
            // it'll unexpectedly affect the date (e.g. it'll think that the 05-01-2015)
            // is the UTC time, and hence it'll make it 04-30-2015, due to GMT-4 time zone..
            // Hence, we'll need to use moment js to "counter" this effect...
            // We might want to think of better approach, as we could have more and more
            // dates that we will be capturing, and this is indeed a source of confusion.
            viewModel.startDate = employeeProfileDomainModel.start_date ? new Date(moment(employeeProfileDomainModel.start_date).format()) : null;
            viewModel.endDate = employeeProfileDomainModel.end_date ? new Date(moment(employeeProfileDomainModel.end_date).format()) : null;
            viewModel.startDateForDisplay = function() {
                return this.startDate ? moment(this.startDate).format(DATE_FORMAT_STRING) : null;
            };

            viewModel.endDateForDisplay = function() {
                return this.endDate ? moment(this.endDate).format(DATE_FORMAT_STRING) : null;
            };

            viewModel.benefitStartDate = employeeProfileDomainModel.benefit_start_date ? new Date(moment(employeeProfileDomainModel.benefit_start_date).format()) : null;

            viewModel.benefitStartDateForDisplay = function() {
                return this.benefitStartDate ? moment(this.benefitStartDate).format(DATE_FORMAT_STRING) : null;
            };

            return viewModel;
        };

        var mapViewToDomainModel = function(employeeProfileViewModel) {
            var domainModel = {};

            domainModel.id = employeeProfileViewModel.id;
            domainModel.job_title = employeeProfileViewModel.jobTitle;
            domainModel.start_date = employeeProfileViewModel.startDate ? moment(employeeProfileViewModel.startDate).format(STORAGE_DATE_FORMAT_STRING) : null;
            domainModel.end_date = employeeProfileViewModel.endDate ? moment(employeeProfileViewModel.endDate).format(STORAGE_DATE_FORMAT_STRING) : null;
            domainModel.employment_type = employeeProfileViewModel.employmentType;
            domainModel.employment_status = employeeProfileViewModel.employmentStatus;
            domainModel.person = employeeProfileViewModel.personId;
            domainModel.company = employeeProfileViewModel.companyId;
            domainModel.department = employeeProfileViewModel.department.id;
            domainModel.benefit_start_date = employeeProfileViewModel.benefitStartDate? moment(employeeProfileViewModel.benefitStartDate).format(STORAGE_DATE_FORMAT_STRING) : domainModel.start_date;
            domainModel.employee_number = employeeProfileViewModel.employeeNumber;
            domainModel.manager = employeeProfileViewModel.manager ? employeeProfileViewModel.manager.id : null;

            return domainModel;
        };

        var mapTerminationViewToDomainModel = function(terminationViewModel) {
            var domainModel = {};

            domainModel.person_id = terminationViewModel.personId;
            domainModel.company_id = terminationViewModel.companyId;
            domainModel.end_date = terminationViewModel.endDate ? moment(terminationViewModel.endDate).format(STORAGE_DATE_FORMAT_STRING) : null;

            return domainModel;
        };

        var initializeCompanyEmployees = function(compId){
            return EmployeeProfileRepository.ByCompany.query({companyId:compId})
            .$promise.then(function(profiles){
                _cachedEmployeeProfiles = profiles;
                return _cachedEmployeeProfiles;
            });
        };

        var searchEmployees = function(term){
            return _.filter(_cachedEmployeeProfiles, function(employee){
              var fullName = employee.first_name + ' ' + employee.last_name;
              return fullName.toLowerCase().indexOf(term.toLowerCase()) > -1;
            });
        };

        var searchEmployeesByEmployeeNumber = function(employeeNumber) {
            return _.filter(_cachedEmployeeProfiles, function(employee) {
              return employee.employee_number && employeeNumber
                && employee.employee_number.toLowerCase() == employeeNumber.toLowerCase();
            });
        };

        return {
            isFullTimeEmploymentType: isFullTimeEmploymentType,
            initializeCompanyEmployees: initializeCompanyEmployees,
            searchEmployees: searchEmployees,
            searchEmployeesByEmployeeNumber: searchEmployeesByEmployeeNumber,

            getEmployeeProfileForPersonCompany: function(personId, companyId) {
                var deferred = $q.defer();

                EmployeeProfileRepository.ByPersonCompany.get({personId:personId, companyId:companyId})
                .$promise.then(function(profile) {
                    var viewModel = mapDomainToViewModel(profile);
                    deferred.resolve(viewModel);
                },
                function(error){
                    // In case no record found, return an "empty" profile
                    if (error.status === 404) {
                        deferred.resolve({ "personId":personId, "companyId":companyId });
                    } else {
                        deferred.reject(error);
                    }
                });

                return deferred.promise;
            },

            getEmployeeProfileForCompanyUser: function(companyId, userId) {
                var deferred = $q.defer();

                EmployeeProfileRepository.ByCompanyUser.get({userId:userId, companyId:companyId})
                .$promise.then(function(profile) {
                    var viewModel = mapDomainToViewModel(profile);
                    deferred.resolve(viewModel);
                },
                function(error){
                    // In case no record found, return an "empty" profile
                    if (error.status === 404) {
                        PersonService.getSelfPersonInfo(userId)
                        .then(function(person) {
                            deferred.resolve({ "personId":person.id, "companyId":companyId })
                        },
                        function(error) {
                            deferred.reject(error);
                        });
                    } else {
                        deferred.reject(error);
                    }
                });

                return deferred.promise;
            },

            saveEmployeeProfile: function(employeeProfileToSave) {
                var deferred = $q.defer();

                var domainModel = mapViewToDomainModel(employeeProfileToSave)
                if (domainModel.id) {
                    // This is an update
                    EmployeeProfileRepository.ById.update({id:domainModel.id}, domainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(mapDomainToViewModel(response));
                        initializeCompanyEmployees(domainModel.company);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    // This is to create a new profile
                    // Use the person Id here purely as a dummy ID to get the
                    // routing match
                    EmployeeProfileRepository.ById.save({id:domainModel.person}, domainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(mapDomainToViewModel(response));
                        initializeCompanyEmployees(domainModel.company);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                };

                return deferred.promise;
            },

            terminateEmployee: function(terminationData) {
                var domainModel = mapTerminationViewToDomainModel(terminationData);

                var deferred = $q.defer();

                EmployeeManagementEmployeeTerminationRepository.ByCompany.save({company_id: terminationData.companyId}, domainModel)
                .$promise.then(function(response) {
                    deferred.resolve(mapDomainToViewModel(response.output_data));
                },
                function(error){
                    deferred.reject(error);
                });

                return deferred.promise;
            },


        };
    }
]);
