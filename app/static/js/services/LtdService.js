var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LtdService', 
    ['$q',
    'LtdRepository',
    function ($q, LtdRepository){
        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};
            
            viewModel.plan_id = planDomainModel.id;
            viewModel.plan_name = planDomainModel.name;
            viewModel.plan_broker = planDomainModel.user;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = companyPlanDomainModel.ltd_insurance_plan ? 
                mapPlanDomainToViewModel(companyPlanDomainModel.ltd_insurance_plan) :
                {};

            viewModel.company_plan_id = companyPlanDomainModel.id;
            viewModel.percentage_of_salary = companyPlanDomainModel.percentage_of_salary;
            viewModel.max_benefit_monthly = companyPlanDomainModel.max_benefit_monthly;
            viewModel.duration = companyPlanDomainModel.duration;
            viewModel.created_date_for_display = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;
            
            return viewModel;
        };

        var mapUserCompanyPlanDomainToViewModel = function(userCompanyPlanDomainModel) {
            var viewModel = userCompanyPlanDomainModel.company_ltd_insurance ? 
                mapCompanyPlanDomainToViewModel(userCompanyPlanDomainModel.company_ltd_insurance) :
                {};

            viewModel.user_company_plan_id = userCompanyPlanDomainModel.id;
            viewModel.plan_owner = userCompanyPlanDomainModel.user;
            viewModel.last_update_date_time = moment(userCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
        
            return viewModel;
        };

        var mapPlanViewToDomainModel = function(planViewModel) {
            var domainModel = {};
            
            domainModel.id = planViewModel.plan_id;
            domainModel.name = planViewModel.plan_name;
            domainModel.user = planViewModel.plan_broker;

            return domainModel;
        };

        var mapCompanyPlanViewToDomainModel = function(companyPlanViewModel) {
            var domainModel = {};

            domainModel.id = companyPlanViewModel.company_plan_id;
            domainModel.percentage_of_salary = companyPlanViewModel.percentage_of_salary;
            domainModel.max_benefit_monthly = companyPlanViewModel.max_benefit_monthly;
            domainModel.duration = companyPlanViewModel.duration;
            domainModel.company = companyPlanViewModel.company;

            domainModel.ltd_insurance_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            return domainModel;
        };

        var mapUserCompanyPlanViewToDomainModel = function(userCompanyPlanViewModel) {
            var domainModel = {};

            domainModel.id = userCompanyPlanViewModel.user_company_plan_id;
            domainModel.user = userCompanyPlanViewModel.plan_owner;

            domainModel.company_ltd_insurance = mapCompanyPlanViewToDomainModel(userCompanyPlanViewModel);

            return domainModel;
        };

        return {
            getLtdPlansForCompany: function(companyId) {
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

            enrollLtdPlanForUser: function(userId, companyLtdPlanToEnroll) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                var userPlan = companyLtdPlanToEnroll;
                userPlan.plan_owner = userId;

                var planDomainModel = mapUserCompanyPlanViewToDomainModel(companyLtdPlanToEnroll);
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

            getUserEnrolledLtdPlanByUser: function(userId) {
                var deferred = $q.defer();

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
                
                return deferred.promise; 
            }
        }; 
    }
]);
