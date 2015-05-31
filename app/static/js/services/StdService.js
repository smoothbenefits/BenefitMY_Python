var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('StdService', 
    ['$q', 'StdRepository', 'EmployeeProfileService',
    function ($q, StdRepository, EmployeeProfileService){
        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};
            
            viewModel.planId = planDomainModel.id;
            viewModel.planName = planDomainModel.name;
            viewModel.planBroker = planDomainModel.user;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = companyPlanDomainModel.std_insurance_plan ? 
                mapPlanDomainToViewModel(companyPlanDomainModel.std_insurance_plan) :
                {};

            viewModel.companyPlanId = companyPlanDomainModel.id;
            viewModel.percentageOfSalary = companyPlanDomainModel.percentage_of_salary;
            viewModel.maxBenefitWeekly = companyPlanDomainModel.max_benefit_weekly;
            viewModel.duration = companyPlanDomainModel.duration;
            viewModel.rate = Number(companyPlanDomainModel.rate);
            viewModel.paidBy = companyPlanDomainModel.paid_by;
            viewModel.eliminationPeriodInDays = companyPlanDomainModel.elimination_period_in_days;
            viewModel.createdDateForDisplay = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;
            viewModel.employerContributionPercentage = companyPlanDomainModel.employer_contribution_percentage;
            
            return viewModel;
        };

        var mapUserCompanyPlanDomainToViewModel = function(userCompanyPlanDomainModel) {
            var viewModel = userCompanyPlanDomainModel.company_std_insurance ? 
                mapCompanyPlanDomainToViewModel(userCompanyPlanDomainModel.company_std_insurance) :
                {};

            viewModel.userCompanyPlanId = userCompanyPlanDomainModel.id;
            viewModel.planOwner = userCompanyPlanDomainModel.user;
            viewModel.lastUpdateDateTime = moment(userCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
        
            return viewModel;
        };

        var mapPlanViewToDomainModel = function(planViewModel) {
            var domainModel = {};
            
            domainModel.id = planViewModel.planId;
            domainModel.name = planViewModel.planName;
            domainModel.user = planViewModel.planBroker;

            return domainModel;
        };

        var mapCompanyPlanViewToDomainModel = function(companyPlanViewModel) {
            var domainModel = {};

            domainModel.id = companyPlanViewModel.companyPlanId;
            domainModel.percentage_of_salary = companyPlanViewModel.percentageOfSalary;
            domainModel.max_benefit_weekly = companyPlanViewModel.maxBenefitWeekly;
            domainModel.duration = companyPlanViewModel.duration;
            domainModel.company = companyPlanViewModel.company;
            domainModel.rate = companyPlanViewModel.rate;
            domainModel.elimination_period_in_days = companyPlanViewModel.eliminationPeriodInDays;
            domainModel.paid_by = companyPlanViewModel.paidBy;
            domainModel.employer_contribution_percentage = companyPlanViewModel.employerContributionPercentage;

            domainModel.std_insurance_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            return domainModel;
        };

        var mapUserCompanyPlanViewToDomainModel = function(userCompanyPlanViewModel) {
            var domainModel = {};

            domainModel.id = userCompanyPlanViewModel.userCompanyPlanId;
            domainModel.user = userCompanyPlanViewModel.planOwner;
            domainModel.total_premium_per_period = userCompanyPlanViewModel.employeePremium;

            domainModel.company_std_insurance = mapCompanyPlanViewToDomainModel(userCompanyPlanViewModel);

            return domainModel;
        };

        return {
            
            paidByParties: ['Employee', 'Employer'],

            getStdPlansForCompany: function(companyId) {
                var deferred = $q.defer();

                StdRepository.CompanyPlanByCompany.query({companyId:companyId})
                .$promise.then(function(plans) {
                    var planViewModels = [];
                    _.each(plans, function(companyPlan) {
                        planViewModels.push(mapCompanyPlanDomainToViewModel(companyPlan));
                    });
                    deferred.resolve(planViewModels);
                },
                function(error){
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            getEmployeePremiumForUserCompanyStdPlan: function(userId, stdPlan) {
                var deferred = $q.defer();

                if (!stdPlan) {
                    deferred.resolve(0);
                } else {
                    var companyId = stdPlan.company;
                    EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, userId).then(function(profile) {
                        var employeeContribution = 1 - (stdPlan.employerContributionPercentage / 100);
                        if (employeeContribution === 0) {
                            deferred.resolve(0.0);
                        }

                        var salary = profile.annualBaseSalary;
                        if (_.isNaN(salary)) {
                            deferred.resolve(null);
                        }

                        var maxBenefitAnnually = stdPlan.maxBenefitWeekly * 52;
                        var benefitPercentage = (stdPlan.percentageOfSalary / 100);

                        var maxBenefit = Math.min(salary * benefitPercentage, maxBenefitAnnually); // Max benefit cannot exceed preset cap
                        var rate = stdPlan.rate;
                        var rateBase = 10;
                        
                        var numOfPeriods = 26; // biweekly

                        var premium = (maxBenefit * (rate / rateBase) * employeeContribution / numOfPeriods).toFixed(2);

                        deferred.resolve(premium);
                    }, function(error) {
                        deferred.reject(error);
                    });
                }

                return deferred.promise;
            },

            addPlanForCompany: function(companyStdPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                var companyPlanDomainModel = mapCompanyPlanViewToDomainModel(companyStdPlanToSave);

                // Create the plan first
                StdRepository.PlanById.save({id:companyPlanDomainModel.std_insurance_plan.user}, companyPlanDomainModel.std_insurance_plan)
                .$promise.then(function(newPlan){

                    // Now enroll the company with this plan
                    companyPlanDomainModel.std_insurance_plan = newPlan.id;
                    companyPlanDomainModel.company = companyId;

                    StdRepository.CompanyPlanByCompany.save({companyId:companyId}, companyPlanDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });

                },
                function(error){
                    deferred.reject(error)
                });
                
                return deferred.promise;
            },

            deleteCompanyStdPlan: function(companyStdPlanIdToDelete) {
                var deferred = $q.defer();

                StdRepository.CompanyPlanById.delete({id:companyStdPlanIdToDelete})
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error) {
                    deferred.reject(error);
                });
                
                return deferred.promise; 
            },

            deleteStdPlansForUser: function(userId) {
                var requests = [];

                StdRepository.CompanyUserPlanByUser.query({userId:userId})
                .$promise.then(function(plans) {
                    _.each(plans, function(plan) {
                        var deferred = $q.defer();
                        requests.push(deferred);

                        StdRepository.CompanyUserPlanById.delete({id:plan.id})
                        .$promise.then(function(response){
                            deferred.resolve(response);
                        },
                        function(error) {
                            deferred.reject(error);
                        })
                    });
                });

                return $q.all(requests);
            },

            enrollStdPlanForUser: function(userId, companyStdPlanToEnroll) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                var userPlan = companyStdPlanToEnroll;
                userPlan.planOwner = userId;

                var planDomainModel = mapUserCompanyPlanViewToDomainModel(companyStdPlanToEnroll);
                planDomainModel.company_std_insurance = planDomainModel.company_std_insurance.id;

                StdRepository.CompanyUserPlanByUser.query({userId:userId})
                .$promise.then(function(userPlans) {
                    if (userPlans.length > 0) {
                        planDomainModel.id = userPlans[0].id;
                        StdRepository.CompanyUserPlanById.update({id:planDomainModel.id}, planDomainModel)
                        .$promise.then(function(response) {
                            deferred.resolve(response);
                        },
                        function(error){
                            deferred.reject(error);
                        });
                    } else {
                        StdRepository.CompanyUserPlanByUser.save({userId:userId}, planDomainModel)
                        .$promise.then(function(response) {
                            deferred.resolve(response);
                        },
                        function(error){
                            deferred.reject(error);
                        });
                    }
                },
                function(error) {
                    deferred.reject(error);
                }); 
                
                return deferred.promise; 
            },

            getUserEnrolledStdPlanByUser: function(userId) {
                var deferred = $q.defer();

                StdRepository.CompanyUserPlanByUser.query({userId:userId})
                .$promise.then(function(plans) {

                    var plan = plans.length > 0 ? 
                        mapUserCompanyPlanDomainToViewModel(plans[0]) :
                        null;

                    deferred.resolve(plan);
                },
                function(error){
                    deferred.reject(error);
                });
                
                return deferred.promise; 
            }
        }; 
    }
]);
