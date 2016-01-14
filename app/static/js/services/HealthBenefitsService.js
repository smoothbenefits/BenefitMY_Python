var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('HealthBenefitsService',
    ['$q',
     'PersonService',
     'CompensationService',
     'EmployeeProfileService',
     'UserService',
     'CompanyGroupHealthBenefitsPlanOptionRepository',
     'benefitListRepository',
    function (
        $q,
        PersonService,
        CompensationService,
        EmployeeProfileService,
        UserService,
        CompanyGroupHealthBenefitsPlanOptionRepository,
        benefitListRepository){

        var getCompanyGroupPlanOptionDomainModel = function(companyPlanOptionId, companyGroups) {
            var domainModel = [];

            _.each(companyGroups, function(companyGroupModel) {
                domainModel.push({ 
                    'company_benefit_plan_option': companyPlanOptionId,
                    'company_group': companyGroupModel.id 
                });
            }); 

            return domainModel;
        };

        var linkCompanyHealthBenefitPlanOptionToCompanyGroups = function(companyPlanOptionId, companyGroups) {
            var deferred = $q.defer();

            var companyGroupPlanDomainModel = getCompanyGroupPlanOptionDomainModel(
                    companyPlanOptionId,
                    companyGroups
                );

            CompanyGroupHealthBenefitsPlanOptionRepository.ByCompanyPlan.update({companyPlanId:companyPlanOptionId}, companyGroupPlanDomainModel
              , function (successResponse) {
                  deferred.resolve(successResponse);
                }
              , function(errorResponse) {
                  deferred.reject(errorResponse);
                }
            );

            return deferred.promise;
        };

        var getPlansForCompanyGroup = function(companyId, companyGroupId) {
            var deferred = $q.defer();

            if (!companyId) {
                deferred.reject('Must specify a valid company ID');
            }
            else if(!companyGroupId){
                deferred.resolve([]);
            }
            else{
                benefitListRepository.get({clientId:companyId})
                .$promise.then(
                    function(response) {
                        var availableBenefits = response.benefits;
                        var filteredBenefits = [];

                        _.each(availableBenefits, function(benefit) {
                            if (_.some(benefit.company_groups, function(company_group) {
                                    return company_group.company_group.id == companyGroupId; })) {
                                filteredBenefits.push(benefit);
                            }    
                        });

                        deferred.resolve(filteredBenefits);
                    },
                    function(errors) {
                        deferred.reject(errors);
                    }
                );
            }

            return deferred.promise;
        };

    return {

      linkCompanyHealthBenefitPlanOptionToCompanyGroups: linkCompanyHealthBenefitPlanOptionToCompanyGroups,
      getPlansForCompanyGroup: getPlansForCompanyGroup
    };
  }
]);
