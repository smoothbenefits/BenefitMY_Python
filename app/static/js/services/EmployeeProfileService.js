var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployeeProfileService', 
    ['$q',
    'EmployeeProfileRepository',
    'peopleRepository',
    function ($q, EmployeeProfileRepository, peopleRepository){
        var mapDomainToViewModel = function(employeeProfileDomainModel) {
            var viewModel = {};
            
            viewModel.id = employeeProfileDomainModel.id;
            viewModel.jobTitle = employeeProfileDomainModel.job_title;
            viewModel.annualBaseSalary = Number(employeeProfileDomainModel.annual_base_salary);
            viewModel.employmentType = employeeProfileDomainModel.employment_type;
            viewModel.employmentStatus = employeeProfileDomainModel.employment_status;
            viewModel.personId = employeeProfileDomainModel.person;
            viewModel.companyId = employeeProfileDomainModel.company;
            viewModel.lastUpdateDateTime = moment(employeeProfileDomainModel.updated_at).format(DATE_FORMAT_STRING);

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

            return viewModel;
        };

        var mapViewToDomainModel = function(employeeProfileViewModel) {
            var domainModel = {};
            
            domainModel.id = employeeProfileViewModel.id; 
            domainModel.job_title = employeeProfileViewModel.jobTitle;
            domainModel.annual_base_salary = employeeProfileViewModel.annualBaseSalary;
            domainModel.start_date = employeeProfileViewModel.startDate ? moment(employeeProfileViewModel.startDate).format(STORAGE_DATE_FORMAT_STRING) : null;
            domainModel.end_date = employeeProfileViewModel.endDate ? moment(employeeProfileViewModel.endDate).format(STORAGE_DATE_FORMAT_STRING) : null;
            domainModel.employment_type = employeeProfileViewModel.employmentType;
            domainModel.employment_status = employeeProfileViewModel.employmentStatus;
            domainModel.person = employeeProfileViewModel.personId;
            domainModel.company = employeeProfileViewModel.companyId;

            return domainModel;
        };

        return {
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
                        peopleRepository.ByUser.get({userId:userId})
                        .$promise.then(function(person) {
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
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    // This is to create a new profile
                    EmployeeProfileRepository.ById.save({id:domainModel.id}, domainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(mapDomainToViewModel(response));
                    },
                    function(error){
                        deferred.reject(error);
                    });
                };

                return deferred.promise; 
            }
        }; 
    }
]);
