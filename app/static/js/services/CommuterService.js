var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CommuterService',
    ['$q',
    'CommuterRepository',
    'PersonService',
    function ($q, CommuterRepository, PersonService){

        var deductionPeriods = [
                {'value':'Monthly', 'displayName':'Monthly'},
                {'value':'PerPayPeriod', 'displayName':'Per Pay Period'}];

        var benefitEnablementOptions = [
                {'value':'ParkingOnly', 'displayName':'Parking Only'},
                {'value':'TransitOnly', 'displayName':'Transit Only'},
                {'value':'Both', 'displayName':'Both Parking and Transit'}];

        var mapEnablementOptionToStatus = function(enablementOption) {
            if (!enablementOption) {
                return null;
            }

            var statusMap = {};

            if (enablementOption) {
                if (enablementOption.value==='Both' || enablementOption.value==='ParkingOnly') {
                    statusMap.enableParkingBenefit = true;
                }
                if (enablementOption.value==='Both' || enablementOption.value==='TransitOnly') {
                    statusMap.enableTransitBenefit = true;
                }
            }

            return statusMap;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = {};

            viewModel.companyPlanId = companyPlanDomainModel.id;
            viewModel.planName = companyPlanDomainModel.plan_name;
            viewModel.employerTransitContribution = convertToNumber(companyPlanDomainModel.employer_transit_contribution);
            viewModel.employerParkingContribution = convertToNumber(companyPlanDomainModel.employer_parking_contribution);
            viewModel.deductionPeriod = companyPlanDomainModel.deduction_period;
            viewModel.createdDateForDisplay = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;

            if (companyPlanDomainModel.enable_transit_benefit && companyPlanDomainModel.enable_parking_benefit) {
                viewModel.benefitEnablementOption = _.find(benefitEnablementOptions, { 'value':'Both'});
            } else if (companyPlanDomainModel.enable_transit_benefit) {
                viewModel.benefitEnablementOption = _.find(benefitEnablementOptions, { 'value':'TransitOnly'});
            } else if (companyPlanDomainModel.enable_parking_benefit) {
                viewModel.benefitEnablementOption = _.find(benefitEnablementOptions, { 'value':'ParkingOnly'});
            }

            return viewModel;
        };

        var mapPersonCompanyPlanDomainToViewModel = function(personCompanyPlanDomainModel) {
            var viewModel = {};
            viewModel.companyPlan = personCompanyPlanDomainModel.company_commuter_plan ?
                mapCompanyPlanDomainToViewModel(personCompanyPlanDomainModel.company_commuter_plan) :
                {};

            viewModel.personCompanyPlanId = personCompanyPlanDomainModel.id;
            viewModel.planOwner = personCompanyPlanDomainModel.person;
            viewModel.lastUpdateDateTime = moment(personCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
            viewModel.monthlyAmountTransitPreTax = convertToNumber(personCompanyPlanDomainModel.monthly_amount_transit_pre_tax);
            viewModel.monthlyAmountTransitPostTax = convertToNumber(personCompanyPlanDomainModel.monthly_amount_transit_post_tax);
            viewModel.monthlyAmountParking = convertToNumber(personCompanyPlanDomainModel.monthly_amount_parking);

            return viewModel;
        };

        var mapCompanyPlanViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.id = viewModel.companyPlanId;
            domainModel.company = viewModel.company;
            domainModel.plan_name = viewModel.planName;
            domainModel.deduction_period = viewModel.deductionPeriod;

            var benefitEnablementStatus = mapEnablementOptionToStatus(viewModel.benefitEnablementOption);

            if (benefitEnablementStatus) {
                if (benefitEnablementStatus.enableParkingBenefit) {
                    domainModel.enable_parking_benefit = true;
                }
                if (benefitEnablementStatus.enableTransitBenefit) {
                    domainModel.enable_transit_benefit = true;
                }
            }

            domainModel.employer_parking_contribution = domainModel.enable_parking_benefit && viewModel.employerParkingContribution
                                                        ? viewModel.employerParkingContribution
                                                        : 0;
            domainModel.employer_transit_contribution = domainModel.enable_transit_benefit && viewModel.employerTransitContribution
                                                        ? viewModel.employerTransitContribution
                                                        : 0;

            return domainModel;
        };

        var mapPersonCompanyPlanViewToDomainModel = function(personCompanyPlanViewModel) {
            var domainModel = {};

            domainModel.id = personCompanyPlanViewModel.personCompanyPlanId;
            domainModel.person = personCompanyPlanViewModel.planOwner;
            domainModel.company_commuter_plan = mapCompanyPlanViewToDomainModel(personCompanyPlanViewModel.companyPlan);

            domainModel.monthly_amount_parking = domainModel.company_commuter_plan.enable_parking_benefit && personCompanyPlanViewModel.monthlyAmountParking
                                                 ? personCompanyPlanViewModel.monthlyAmountParking
                                                 : 0;
            domainModel.monthly_amount_transit_pre_tax = domainModel.company_commuter_plan.enable_transit_benefit && personCompanyPlanViewModel.monthlyAmountTransitPreTax
                                                         ? personCompanyPlanViewModel.monthlyAmountTransitPreTax
                                                         : 0;
            domainModel.monthly_amount_transit_post_tax = domainModel.company_commuter_plan.enable_transit_benefit && personCompanyPlanViewModel.monthlyAmountTransitPostTax
                                                          ? personCompanyPlanViewModel.monthlyAmountTransitPostTax
                                                          : 0;

            return domainModel;
        };

        var getPlansForCompany = function(companyId) {
            var deferred = $q.defer();

            CommuterRepository.CompanyPlanByCompany.query({companyId:companyId})
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

        var convertToNumber = function(rawNumber) {
            return rawNumber != null && rawNumber != undefined ? Number(rawNumber) : null;
        };

        var computeTotalMonthlyTransitAllowance = function(personPlan) {
            return (personPlan.companyPlan.employerTransitContribution
                + personPlan.monthlyAmountTransitPreTax
                + personPlan.monthlyAmountTransitPostTax)
                .toFixed(2);
        };

        var computeTotalMonthlyParkingAllowance = function(personPlan) {
            return (personPlan.companyPlan.employerParkingContribution
                + personPlan.monthlyAmountParking)
                .toFixed(2);
        };

        return {

            deductionPeriods: deductionPeriods,

            benefitEnablementOptions: benefitEnablementOptions,

            getPlansForCompany: getPlansForCompany,

            mapEnablementOptionToStatus: mapEnablementOptionToStatus,

            computeTotalMonthlyTransitAllowance: computeTotalMonthlyTransitAllowance,

            computeTotalMonthlyParkingAllowance: computeTotalMonthlyParkingAllowance,

            getBlankPlanForCompany: function(companyId) {
                var deferred = $q.defer();

                var blankCompanyPlan = {};

                // Setup company
                blankCompanyPlan.company = companyId;

                deferred.resolve(blankCompanyPlan);

                return deferred.promise;
            },

            addPlanForCompany: function(companyPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                var companyPlanDomainModel = mapCompanyPlanViewToDomainModel(companyPlanToSave);
                companyPlanDomainModel.company = companyId;

                CommuterRepository.CompanyPlanById.save({id:companyId}, companyPlanDomainModel)
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error){
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            deleteCompanyPlan: function(companyPlanIdToDelete) {
                var deferred = $q.defer();

                CommuterRepository.CompanyPlanById.delete({id:companyPlanIdToDelete})
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            deletePlansForUser: function(userId, company) {
                var requests = [];

                PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
                    CommuterRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
                    .$promise.then(function(plans) {
                        _.each(plans, function(plan) {
                            var deferred = $q.defer();
                            requests.push(deferred);

                            CommuterRepository.CompanyPersonPlanById.delete({id:plan.id})
                            .$promise.then(function(response){
                                deferred.resolve(response);
                            },
                            function(error) {
                                deferred.reject(error);
                            })
                        });
                    });
                });

                return $q.all(requests);
            },

            savePersonPlan: function(personPlanToSave, updateReason) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                personPlanToSave.updateReason = updateReason;

                var planDomainModel = mapPersonCompanyPlanViewToDomainModel(personPlanToSave);

                // "Flatten out" any nested structure for the POST to work
                planDomainModel.company_commuter_plan = planDomainModel.company_commuter_plan.id;

                if (planDomainModel.id){
                    CommuterRepository.CompanyPersonPlanById.update({id:planDomainModel.id}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    CommuterRepository.CompanyPersonPlanById.save({id:personPlanToSave.planOwner}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                }

                return deferred.promise;
            },

            getPersonPlanByUser: function(userId, company, getBlankPlanIfNoneFound) {
                var deferred = $q.defer();
                getPlansForCompany(company).then(function(companyPlans){
                    if(!companyPlans || companyPlans.length<=0){
                        deferred.resolve(undefined);
                    }
                    else{
                        // Just like all other benefits, assuming single plan for company now
                        var companyPlan = companyPlans[0];

                        PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
                            CommuterRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
                            .$promise.then(function(personPlans) {
                                if (personPlans.length > 0) {
                                    // Found existing person enrolled plans, for now, take the first
                                    // one.
                                    deferred.resolve(mapPersonCompanyPlanDomainToViewModel(personPlans[0]));
                                } else {
                                    // The person does not have enrolled plans yet.
                                    // If indicated so, construct and return an structured
                                    // blank person plan.
                                    // Or else, return null;
                                    if (getBlankPlanIfNoneFound) {
                                        var blankPersonPlan = {
                                          'monthlyAmountParking': 0,
                                          'monthlyAmountTransitPreTax': 0,
                                          'monthlyAmountTransitPostTax': 0
                                        };

                                        // Setup person plan owner
                                        blankPersonPlan.planOwner = personInfo.id;

                                        // Setup the company Plan to link
                                        blankPersonPlan.companyPlan = companyPlan;

                                        deferred.resolve(blankPersonPlan);
                                    }
                                    else {
                                        deferred.resolve(null);
                                    }
                                }
                            },
                            function(error) {
                                deferred.reject(error);
                            });
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
