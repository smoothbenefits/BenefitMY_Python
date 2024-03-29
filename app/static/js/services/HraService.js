var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('HraService',
    ['$q',
    'HraRepository',
    'PersonService',
    'CompanyGroupHraPlanRepository',
    'UserService',
    function (
        $q, 
        HraRepository, 
        PersonService,
        CompanyGroupHraPlanRepository,
        UserService){

        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};

            viewModel.planId = planDomainModel.id;
            viewModel.planName = planDomainModel.name;
            viewModel.planDescription = planDomainModel.description;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = companyPlanDomainModel.hra_plan ?
                mapPlanDomainToViewModel(companyPlanDomainModel.hra_plan) :
                {};

            viewModel.companyPlanId = companyPlanDomainModel.id;
            viewModel.createdDateForDisplay = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;
            viewModel.companyGroups = companyPlanDomainModel.company_groups;

            return viewModel;
        };

        var mapPersonCompanyPlanDomainToViewModel = function(personCompanyPlanDomainModel) {
            var viewModel = personCompanyPlanDomainModel.company_hra_plan ?
                mapCompanyPlanDomainToViewModel(personCompanyPlanDomainModel.company_hra_plan) :
                {waived:true};

            viewModel.personCompanyPlanId = personCompanyPlanDomainModel.id;
            viewModel.planOwner = personCompanyPlanDomainModel.person;
            viewModel.lastUpdateDateTime = moment(personCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);

            return viewModel;
        };

        var mapPlanViewToDomainModel = function(planViewModel) {
            var domainModel = {};

            domainModel.id = planViewModel.planId;
            domainModel.name = planViewModel.planName;
            domainModel.description = planViewModel.planDescription;

            return domainModel;
        };

        var mapCompanyPlanViewToDomainModel = function(companyPlanViewModel) {
            var domainModel = {};

            domainModel.id = companyPlanViewModel.companyPlanId;
            domainModel.company = companyPlanViewModel.company;

            domainModel.hra_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            return domainModel;
        };

        var mapPersonCompanyPlanViewToDomainModel = function(personCompanyPlanViewModel) {
            var domainModel = {};

            domainModel.id = personCompanyPlanViewModel.personCompanyPlanId;
            domainModel.person = personCompanyPlanViewModel.planOwner;

            domainModel.company_hra_plan = mapCompanyPlanViewToDomainModel(personCompanyPlanViewModel);

            domainModel.record_reason_note = personCompanyPlanViewModel.updateReason.notes;
            domainModel.record_reason = personCompanyPlanViewModel.updateReason.selectedReason.id;

            return domainModel;
        };

        var getPlansForCompany = function(companyId) {
            var deferred = $q.defer();

            HraRepository.CompanyPlanByCompany.query({companyId:companyId})
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

        var getPlansForCompanyGroup = function(companyGroupId) {
            var deferred = $q.defer();
            if(!companyGroupId){
                deferred.resolve([]);
            }
            else{
                CompanyGroupHraPlanRepository.ByCompanyGroup.query({companyGroupId:companyGroupId})
                .$promise.then(function(companyGroupPlans) {
                    var resultPlans = [];
                    
                    _.each(companyGroupPlans, function(companyGroupPlan) {
                        var companyPlan = companyGroupPlan.company_hra_plan;
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

        var mapCreatePlanViewToCompanyGroupPlanDomainModel = function(createPlanViewModel) {
            var domainModel = [];

            _.each(createPlanViewModel.selectedCompanyGroups, function(companyGroupModel) {
                domainModel.push({ 
                    'company_hra_plan': createPlanViewModel.companyPlanId,
                    'company_group': companyGroupModel.id 
                });
            }); 
  
            return domainModel;
        };

        var linkCompanyHraPlanToCompanyGroups = function(companyPlanId, companyGroupPlanModels){
            var deferred = $q.defer();

            CompanyGroupHraPlanRepository.ByCompanyPlan.update(
                { pk: companyPlanId }, 
                companyGroupPlanModels, 
                function (successResponse) {
                    deferred.resolve(successResponse);
                }
            );

            return deferred.promise;
        };

        return {

            getPlansForCompany: getPlansForCompany,

            getPlansForCompanyGroup: getPlansForCompanyGroup,

            getBlankPlanForCompany: function(companyId) {
                var deferred = $q.defer();

                var blankCompanyPlan = {};

                // Setup company
                blankCompanyPlan.company = companyId;
                blankCompanyPlan.selectedCompanyGroups = [];

                deferred.resolve(blankCompanyPlan);

                return deferred.promise;
            },

            addPlanForCompany: function(companyPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                var companyPlanDomainModel = mapCompanyPlanViewToDomainModel(companyPlanToSave);

                // Create the plan first
                HraRepository.PlanById.save({id:companyId}, companyPlanDomainModel.hra_plan)
                .$promise.then(function(newPlan){

                    // Now enroll the company with this plan
                    companyPlanDomainModel.hra_plan = newPlan.id;
                    companyPlanDomainModel.company = companyId;

                    HraRepository.CompanyPlanById.save({id:companyId}, companyPlanDomainModel)
                    .$promise.then(function(createdCompanyPlan) {
                        //Now link the company plan with company group
                        companyPlanToSave.companyPlanId = createdCompanyPlan.id;
                        compGroupPlans = mapCreatePlanViewToCompanyGroupPlanDomainModel(companyPlanToSave);
                        linkCompanyHraPlanToCompanyGroups(createdCompanyPlan.id, compGroupPlans).then(
                             function(createdCompanyGroupPlans) {
                                 deferred.resolve(createdCompanyGroupPlans);
                             },
                             function(errors) {
                                 deferred.reject(errors);
                             }
                         );
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

            deleteCompanyPlan: function(companyPlanIdToDelete) {
                var deferred = $q.defer();

                HraRepository.CompanyPlanById.delete({id:companyPlanIdToDelete})
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            savePersonPlan: function(personPlanToSave, updateReason, enrollBenefits) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                personPlanToSave.updateReason = updateReason;

                var planDomainModel = mapPersonCompanyPlanViewToDomainModel(personPlanToSave);

                // "Flatten out" any nested structure for the POST to work
                if (enrollBenefits) {
                  planDomainModel.company_hra_plan = planDomainModel.company_hra_plan.id;
                } else {
                  planDomainModel.company_hra_plan = null;
                }

                if (planDomainModel.id){
                    HraRepository.CompanyPersonPlanById.update({id:planDomainModel.id}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    HraRepository.CompanyPersonPlanById.save({id:personPlanToSave.planOwner}, planDomainModel)
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

                UserService.getUserDataByUserId(userId).then(
                    function(userData) {
                        getPlansForCompanyGroup(userData.companyGroupId).then(function(plans){
                            if(!plans || plans.length<=0){
                                deferred.resolve(undefined);
                            }
                            else{
                                PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
                                    HraRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
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
                                                var blankPersonPlan = {};

                                                // Setup person plan owner
                                                blankPersonPlan.planOwner = personInfo.id;

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
                    },
                    function(errors) {
                        deferred.reject(errors);
                    }
                );

                return deferred.promise;
            }
        };
    }
]);
