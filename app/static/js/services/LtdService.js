var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LtdService',
    ['$q',
    'LtdRepository',
    'EmployeeProfileService',
    function ($q, LtdRepository, EmployeeProfileService){
        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};

            viewModel.planId = planDomainModel.id;
            viewModel.planName = planDomainModel.name;
            viewModel.planBroker = planDomainModel.user;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = companyPlanDomainModel.ltd_insurance_plan ?
                mapPlanDomainToViewModel(companyPlanDomainModel.ltd_insurance_plan) :
                {};

            viewModel.companyPlanId = companyPlanDomainModel.id;
            viewModel.percentageOfSalary = companyPlanDomainModel.percentage_of_salary;
            viewModel.maxBenefitMonthly = companyPlanDomainModel.max_benefit_monthly;
            viewModel.duration = companyPlanDomainModel.duration;
            viewModel.rate = Number(companyPlanDomainModel.rate);
            viewModel.paidBy = companyPlanDomainModel.paid_by;
            viewModel.eliminationPeriodInMonths = companyPlanDomainModel.elimination_period_in_months;
            viewModel.createdDateForDisplay = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;
            viewModel.employerContributionPercentage = companyPlanDomainModel.employer_contribution_percentage;

            return viewModel;
        };

        var mapUserCompanyPlanDomainToViewModel = function(userCompanyPlanDomainModel) {
          var viewModel = {};
          if (userCompanyPlanDomainModel.company_ltd_insurance) {
            viewModel = mapCompanyPlanDomainToViewModel(userCompanyPlanDomainModel.company_ltd_insurance);
          }

          viewModel.userCompanyPlanId = userCompanyPlanDomainModel.id;
          viewModel.planOwner = userCompanyPlanDomainModel.user;
          viewModel.lastUpdateDateTime = moment(userCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
          viewModel.selected = true;
          viewModel.waived = !userCompanyPlanDomainModel.company_ltd_insurance;

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
            domainModel.max_benefit_monthly = companyPlanViewModel.maxBenefitMonthly;
            domainModel.duration = companyPlanViewModel.duration;
            domainModel.rate = companyPlanViewModel.rate;
            domainModel.paid_by = companyPlanViewModel.paidBy;
            domainModel.elimination_period_in_months = companyPlanViewModel.eliminationPeriodInMonths;
            domainModel.company = companyPlanViewModel.company;
            domainModel.employer_contribution_percentage = companyPlanViewModel.employerContributionPercentage;

            domainModel.ltd_insurance_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            //Here is the location to convert age_based_rates
            domainModel.age_based_rates = [];

            return domainModel;
        };

        var mapUserCompanyPlanViewToDomainModel = function(userCompanyPlanViewModel, payPeriod) {
            var domainModel = {};

            domainModel.id = userCompanyPlanViewModel.userCompanyPlanId;
            domainModel.user = userCompanyPlanViewModel.planOwner;

            if (userCompanyPlanViewModel.totalPremium) {
              domainModel.total_premium_per_month = userCompanyPlanViewModel.totalPremium.toFixed(10);
            } else {
              domainModel.total_premium_per_month = null;
            }

            domainModel.company_ltd_insurance = mapCompanyPlanViewToDomainModel(userCompanyPlanViewModel);

            domainModel.record_reason_note = userCompanyPlanViewModel.updateReason.notes;
            domainModel.record_reason = userCompanyPlanViewModel.updateReason.selectedReason.id;

            return domainModel;
        };

        var getLtdPlansForCompany = function(companyId) {
            var deferred = $q.defer();

            LtdRepository.CompanyPlanByCompany.query({companyId:companyId})
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
        };

        return {
            paidByParties: ['Employee', 'Employer'],

            getLtdPlansForCompany: getLtdPlansForCompany,

            getEmployeePremiumForUserCompanyLtdPlan: function(userId, ltdPlan) {
                var deferred = $q.defer();

                if (!ltdPlan) {
                    deferred.resolve(0);
                } else {
                    LtdRepository.CompanyPlanPremiumByUser.get({userId:userId, id:ltdPlan.companyPlanId})
                    .$promise.then(function(premiumInfo) {
                        deferred.resolve({totalPremium:premiumInfo.total,
                            employeePremiumPerPayPeriod: premiumInfo.employee});
                    }, function(error) {
                        deferred.reject(error);
                    });
                }

                return deferred.promise;
            },

            addPlanForCompany: function(companyLtdPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                var companyPlanDomainModel = mapCompanyPlanViewToDomainModel(companyLtdPlanToSave);

                // Create the plan first
                LtdRepository.PlanById.save({id:companyPlanDomainModel.ltd_insurance_plan.user}, companyPlanDomainModel.ltd_insurance_plan)
                .$promise.then(function(newPlan){

                    // Now enroll the company with this plan
                    companyPlanDomainModel.ltd_insurance_plan = newPlan.id;
                    companyPlanDomainModel.company = companyId;

                    LtdRepository.CompanyPlanByCompany.save({companyId:companyId}, companyPlanDomainModel)
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

            deleteCompanyLtdPlan: function(companyLtdPlanIdToDelete) {
                var deferred = $q.defer();

                LtdRepository.CompanyPlanById.delete({id:companyLtdPlanIdToDelete})
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            deleteLtdPlansForUser: function(userId) {
                var requests = [];

                LtdRepository.CompanyUserPlanByUser.query({userId:userId})
                .$promise.then(function(plans) {
                    _.each(plans, function(plan) {
                        var deferred = $q.defer();
                        requests.push(deferred);

                        LtdRepository.CompanyUserPlanById.delete({id:plan.id})
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

            enrollLtdPlanForUser: function(userId,
                                           companyLtdPlanToEnroll,
                                           payPeriod,
                                           updateReason) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                var userPlan = companyLtdPlanToEnroll;
                userPlan.planOwner = userId;
                userPlan.updateReason = updateReason;

                var planDomainModel = mapUserCompanyPlanViewToDomainModel(companyLtdPlanToEnroll, payPeriod);
                planDomainModel.company_ltd_insurance = planDomainModel.company_ltd_insurance.id;

                LtdRepository.CompanyUserPlanByUser.query({userId:userId})
                .$promise.then(function(userPlans) {
                    if (userPlans.length > 0) {
                        planDomainModel.id = userPlans[0].id;
                        LtdRepository.CompanyUserPlanById.update({id:planDomainModel.id}, planDomainModel)
                        .$promise.then(function(response) {
                            deferred.resolve(response);
                        },
                        function(error){
                            deferred.reject(error);
                        });
                    } else {
                        LtdRepository.CompanyUserPlanByUser.save({userId:userId}, planDomainModel)
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

            getUserEnrolledLtdPlanByUser: function(userId, company) {
                var deferred = $q.defer();
                getLtdPlansForCompany(company).then(function(plans){
                    if(!plans || plans.length <= 0){
                        deferred.resolve(undefined);
                    }
                    else{
                        LtdRepository.CompanyUserPlanByUser.query({userId:userId})
                        .$promise.then(function(plans) {

                            var plan = plans.length > 0 ?
                                mapUserCompanyPlanDomainToViewModel(plans[0]) :
                                null;

                            deferred.resolve(plan);
                        },
                        function(error){
                            deferred.reject(error);
                        });
                    }
                });

                return deferred.promise;
            }
        };
    }
]);
