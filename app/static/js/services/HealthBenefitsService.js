var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('HealthBenefitsService',
  ['$q',
   'PersonService',
   'CompensationService',
   'EmployeeProfileService',
   'UserService',
   'CompanyGroupHealthBenefitsPlanOptionRepository',
  function (
      $q,
      PersonService,
      CompensationService,
      EmployeeProfileService,
      UserService,
      CompanyGroupHealthBenefitsPlanOptionRepository){

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

    return {

      linkCompanyHealthBenefitPlanOptionToCompanyGroups: linkCompanyHealthBenefitPlanOptionToCompanyGroups

    };
  }
]);
