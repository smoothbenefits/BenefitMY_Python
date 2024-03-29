var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('StdService',
    ['$q',
     'StdRepository',
     'EmployeeProfileService',
     'AgeRangeService',
     'UserService',
     'CompanyGroupStdInsurancePlanRepository',
    function ($q,
              StdRepository,
              EmployeeProfileService,
              AgeRangeService,
              UserService,
              CompanyGroupStdInsurancePlanRepository){
        var ageRangeService = AgeRangeService(20, 85, 5, 200);
        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};

            viewModel.planId = planDomainModel.id;
            viewModel.planName = planDomainModel.name;
            viewModel.planBroker = planDomainModel.user;

            return viewModel;
        };

        var mapCompanyPlanAgeBasedTableDomainToViewModel = function(ageBasedRates){
            ageBasedRatesTable = [];
            _.each(ageBasedRates, function(ageBasedRateItem){
                ageBasedRatesTable.push({
                    ageMin: ageBasedRateItem.age_min,
                    ageMax: ageBasedRateItem.age_max,
                    rate: Number(ageBasedRateItem.rate).toFixed(4),
                    getAgeRangeForDisplay: function(){return ageRangeService.getAgeRangeForDisplay(this);}
                });
            });
            return ageBasedRatesTable;
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
            viewModel.stepValue = companyPlanDomainModel.benefit_amount_step;
            viewModel.allowUserSelectAmount = companyPlanDomainModel.user_amount_required;
            viewModel.ageBasedRates = mapCompanyPlanAgeBasedTableDomainToViewModel(companyPlanDomainModel.age_based_rates);
            viewModel.companyGroups = companyPlanDomainModel.company_groups;

            return viewModel;
        };

        var mapUserCompanyPlanDomainToViewModel = function(userCompanyPlanDomainModel) {

            var viewModel = {};
            if (userCompanyPlanDomainModel.company_std_insurance) {
              viewModel = mapCompanyPlanDomainToViewModel(userCompanyPlanDomainModel.company_std_insurance);
            }

            viewModel.userCompanyPlanId = userCompanyPlanDomainModel.id;
            viewModel.planOwner = userCompanyPlanDomainModel.user;
            viewModel.lastUpdateDateTime = moment(userCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
            viewModel.selected = true;
            viewModel.waived = !userCompanyPlanDomainModel.company_std_insurance;

            return viewModel;
        };

        var mapPlanViewToDomainModel = function(planViewModel) {
            var domainModel = {};

            domainModel.id = planViewModel.planId;
            domainModel.name = planViewModel.planName;
            domainModel.user = planViewModel.planBroker;

            return domainModel;
        };

        var mapPlanAgeBasedRatesToDomainModal = function(ageBasedRateTable){
            domainTable = [];
            _.each(ageBasedRateTable, function(row){
                if(row && row.rate){
                    domainTable.push({
                        age_min: row.ageMin,
                        age_max: row.ageMax,
                        rate: row.rate
                    });
                }
            });
            return domainTable;
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
            domainModel.user_amount_required = companyPlanViewModel.allowUserSelectAmount;
            domainModel.benefit_amount_step = companyPlanViewModel.stepValue;

            domainModel.std_insurance_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            //Here is the location to convert age_based_rates
            domainModel.age_based_rates = mapPlanAgeBasedRatesToDomainModal(companyPlanViewModel.ageBasedRateTable);

            return domainModel;
        };

        var mapUserCompanyPlanViewToDomainModel = function(userCompanyPlanViewModel, payPeriod) {
            var domainModel = {};

            domainModel.id = userCompanyPlanViewModel.userCompanyPlanId;
            domainModel.user = userCompanyPlanViewModel.planOwner;

            if (userCompanyPlanViewModel.totalPremium) {
              var totalPremium = parseFloat(userCompanyPlanViewModel.totalPremium);
              domainModel.total_premium_per_month = totalPremium.toFixed(10);
            } else {
              domainModel.total_premium_per_month = null;
            }

            domainModel.company_std_insurance = mapCompanyPlanViewToDomainModel(userCompanyPlanViewModel);

            domainModel.record_reason_note = userCompanyPlanViewModel.updateReason.notes;
            domainModel.record_reason = userCompanyPlanViewModel.updateReason.selectedReason.id;

            return domainModel;
        };

        var getStdPlansForCompany = function(companyId) {
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
        };

        var getBlankAgeBasedRateTableViewModel = function(){
            var ageRangeList = ageRangeService.getAgeRangeList();
            var rateTable = [];
            _.each(ageRangeList, function(ageRange){
                rateTable.push({
                    'ageMin' : ageRange.min,
                    'ageMax' : ageRange.max,
                    'getAgeRangeForDisplay': function(){return ageRangeService.getAgeRangeForDisplay(this);}
                });
            });
            _.sortBy(rateTable, 'ageMin');
            return rateTable;
        };

        var mapCreatePlanViewToCompanyGroupPlanDomainModel = function(createdCompanyStdPlan){
            var domainModels = [];
            _.each(createdCompanyStdPlan.selectedCompanyGroups, function(companyGroup){
                domainModels.push({
                    'company_std_insurance_plan': createdCompanyStdPlan.id,
                    'company_group': companyGroup.id
                });
            });
            return domainModels;
        };

        var linkCompanyStdInsurancePlanToCompanyGroups = function(compStdPlanId, compGroupPlanModels){
            return CompanyGroupStdInsurancePlanRepository.ByCompanyPlan.update(
                {pk:compStdPlanId},
                compGroupPlanModels,
                function (successResponse) {
                    return successResponse;
                }
            );
        };

        var getStdPlansForCompanyGroup = function(companyGroupId){
            var deferred = $q.defer();
            if(!companyGroupId){
                deferred.resolve([]);
            }
            else{
                CompanyGroupStdInsurancePlanRepository.ByCompanyGroup.query({companyGroupId:companyGroupId})
                .$promise.then(function(companyGroupPlans) {
                    var resultPlans = [];

                    _.each(companyGroupPlans, function(companyGroupPlan) {
                        var companyPlan = companyGroupPlan.company_std_insurance_plan;
                        resultPlans.push(mapCompanyPlanDomainToViewModel(companyPlan));
                    });

                    deferred.resolve(resultPlans);
                },
                function(failedResponse) {
                    deferred.reject(failedResponse);
                });
            }
            return deferred.promise;
        };


        return {

            paidByParties: ['Employee', 'Employer'],

            getStdPlansForCompany: getStdPlansForCompany,

            getStdPlansForCompanyGroup: getStdPlansForCompanyGroup,

            getTotalPremiumForUserCompanyStdPlan: function(userId, stdPlan, amount) {
                var deferred = $q.defer();

                if (stdPlan.allowUserSelectAmount && _.isNumber(amount)) {
                  amount = parseInt(Math.round(amount / stdPlan.stepValue) * stdPlan.stepValue);
                } else {
                  amount = null;
                }

                var request = {
                  'amount': amount,
                  'user': userId,
                  'companyStdPlan': stdPlan.companyPlanId
                };

                if (!stdPlan) {
                    deferred.resolve(0);
                } else {
                    StdRepository.CompanyPlanPremiumByUser.save(
                      {userId:userId, id:stdPlan.companyPlanId}, request
                    ).$promise.then(function(premiumInfo) {
                      deferred.resolve({
                        totalPremium: Number(premiumInfo.total).toFixed(2),
                        employeePremiumPerPayPeriod: Number(premiumInfo.employee).toFixed(2),
                        effectiveBenefitAmount: Number(premiumInfo.amount).toFixed(2)
                      });
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
                    .$promise.then(function(createdCompanyPlan) {
                        createdCompanyPlan.selectedCompanyGroups = companyStdPlanToSave.selectedCompanyGroups;
                        companyGroupDomainModels = mapCreatePlanViewToCompanyGroupPlanDomainModel(createdCompanyPlan);
                        linkCompanyStdInsurancePlanToCompanyGroups(createdCompanyPlan.id, companyGroupDomainModels)
                        .$promise.then(function(response){
                            deferred.resolve(response);
                        });
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

            enrollStdPlanForUser: function(userId,
                                           userSelectAmount,
                                           companyStdPlanToEnroll,
                                           payPeriod,
                                           updateReason) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                var userPlan = companyStdPlanToEnroll;
                userPlan.planOwner = userId;
                userPlan.updateReason = updateReason;

                var planDomainModel = mapUserCompanyPlanViewToDomainModel(companyStdPlanToEnroll, payPeriod);
                planDomainModel.company_std_insurance = planDomainModel.company_std_insurance.id;
                planDomainModel.user_select_amount = userSelectAmount;

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

                UserService.getUserDataByUserId(userId).then(function(userData){
                    getStdPlansForCompanyGroup(userData.companyGroupId).then(function(plans){
                        if(!plans || plans.length <= 0){
                            deferred.resolve(undefined);
                        }
                        else{
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
                        }
                    });
                });

                return deferred.promise;
            },
            getBlankAgeBasedRateTableViewModel: getBlankAgeBasedRateTableViewModel
        };
    }
]);
