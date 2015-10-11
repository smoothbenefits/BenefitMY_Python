var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('ExtraBenefitService',
    ['$q',
    'ExtraBenefitRepository',
    'PersonService',
    function ($q, ExtraBenefitRepository, PersonService){
        var mapCompanyPlanBenefitItemDomainToViewModel = function(domainModel) {
            var viewModel = {};

            viewModel.benefitItemId = domainModel.id;
            viewModel.companyPlanId = domainModel.company_plan;
            viewModel.name = domainModel.name;
            viewModel.description = domainModel.description;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(domainModel) {
            var viewModel = {};

            viewModel.companyPlanId = domainModel.id;
            viewModel.company = domainModel.company;
            viewModel.planDescription = domainModel.description;
            viewModel.benefitItems = [];

            if (domainModel.benefit_items) {
                _.each(domainModel.benefit_items, function(item) {
                    viewModel.benefitItems.push(mapCompanyPlanBenefitItemDomainToViewModel(item));
                });
            }

            viewModel.createdDateForDisplay = moment(domainModel.created_at).format(DATE_FORMAT_STRING);

            return viewModel;
        };

        var mapPersonCompanyPlanItemDomainToViewModel = function(domainModel) {
            var viewModel = {};

            viewModel.planItemId = domainModel.id;
            viewModel.personCompanyPlanId = domainModel.person_company_extra_benefit_plan;
            viewModel.optIn = domainModel.opt_in;
            viewModel.benefitItem = mapCompanyPlanBenefitItemDomainToViewModel(domainModel.extra_benefit_item);

            return viewModel;
        };

        var mapPersonCompanyPlanDomainToViewModel = function(domainModel) {
            var viewModel = {};

            viewModel.companyPlan = domainModel.company_plan ?
                mapCompanyPlanDomainToViewModel(domainModel.company_plan) :
                {};

            viewModel.personCompanyPlanId = domainModel.id;
            viewModel.planOwner = domainModel.person;
            viewModel.lastUpdateDateTime = moment(domainModel.updated_at).format(DATE_FORMAT_STRING);
            viewModel.planItems = [];

            if (domainModel.plan_items) {
                _.each(domainModel.plan_items, function(item) {
                    viewModel.planItems.push(mapPersonCompanyPlanItemDomainToViewModel(item));
                });
            }

            return viewModel;
        };

        var mapCompanyPlanBenefitItemViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.id = viewModel.benefitItemId;
            domainModel.company_plan = viewModel.companyPlanId;
            domainModel.name = viewModel.name;
            domainModel.description = viewModel.description;

            return domainModel;
        };

        var isPlanBenefitItemEmpty = function(planItemViewModel) {
            return !planItemViewModel.name && !planItemViewModel.description; 
        };

        var mapCompanyPlanViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.id = viewModel.companyPlanId;
            domainModel.company = viewModel.company;
            domainModel.description = viewModel.planDescription;
            domainModel.benefit_items = [];

            if (viewModel.benefitItems) {
                _.each(viewModel.benefitItems, function(item) {
                    // Skip plan items that are empty
                    if (!isPlanBenefitItemEmpty(item)) {
                        domainModel.benefit_items.push(mapCompanyPlanBenefitItemViewToDomainModel(item));
                    }
                });
            }

            return domainModel;
        };

        var mapPersonCompanyPlanItemViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.id = viewModel.planItemId;
            domainModel.person_company_extra_benefit_plan = viewModel.personCompanyPlanId;
            domainModel.opt_in = viewModel.optIn;
            domainModel.extra_benefit_item = viewModel.benefitItem.benefitItemId;

            return domainModel;
        };

        var mapPersonCompanyPlanViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.company_plan = viewModel.companyPlan.companyPlanId;
            domainModel.id = viewModel.personCompanyPlanId;
            domainModel.person = viewModel.planOwner;
            domainModel.plan_items = [];

            if (viewModel.planItems) {
                _.each(viewModel.planItems, function(item) {
                    domainModel.plan_items.push(mapPersonCompanyPlanItemViewToDomainModel(item));
                });
            }

            return domainModel;
        };

        var getPlansForCompany = function(companyId) {
            var deferred = $q.defer();

            ExtraBenefitRepository.CompanyPlanByCompany.query({companyId:companyId})
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

            getPlansForCompany: getPlansForCompany,

            getBlankPlanForCompany: function(companyId) {
                var deferred = $q.defer();

                var blankCompanyPlan = {};

                // Setup company
                blankCompanyPlan.company = companyId;

                // Setup the list to hold benefit items
                blankCompanyPlan.benefitItems = [];
                blankCompanyPlan.benefitItems.push({});

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

                ExtraBenefitRepository.CompanyPlanById.save({id:companyId}, companyPlanDomainModel)
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

                ExtraBenefitRepository.CompanyPlanById.delete({id:companyPlanIdToDelete})
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
                    ExtraBenefitRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
                    .$promise.then(function(plans) {
                        _.each(plans, function(plan) {
                            var deferred = $q.defer();
                            requests.push(deferred);

                            ExtraBenefitRepository.CompanyPersonPlanById.delete({id:plan.id})
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

                if (planDomainModel.id){
                    ExtraBenefitRepository.CompanyPersonPlanById.update({id:planDomainModel.id}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    ExtraBenefitRepository.CompanyPersonPlanById.save({id:personPlanToSave.planOwner}, planDomainModel)
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
                            ExtraBenefitRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
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
                                          'planItems': []
                                        };

                                        // Setup person plan owner
                                        blankPersonPlan.planOwner = personInfo.id;

                                        // Setup the company Plan to link
                                        blankPersonPlan.companyPlan = companyPlan;

                                        // Use the benefit items from the company plan
                                        // to populate the person plan items
                                        blankPersonPlan.planItems = [];
                                        _.each(companyPlan.benefitItems, function(item) {
                                            var planItem = {};
                                            planItem.benefitItem = item;
                                            planItem.optIn = false;

                                            blankPersonPlan.planItems.push(planItem);
                                        });

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
