var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyBenefitAvailabilityService',
  ['$q',
  'CompanyBenefitAvailabilityRepository',
  'UserService',
  function BenefitSummaryService(
    $q,
    CompanyBenefitAvailabilityRepository,
    UserService){

    var filterByCompanyGroup = function(domainModelItem, companyGroupId){
      if(!companyGroupId){
        //If the company group id is not defined, we shall automatically return false;
        return false;
      }

      return _.some(domainModelItem, function(plan){
        return _.some(plan.company_groups, function(company_group){
          return company_group.company_group.id == companyGroupId;
        });
      });
    };

    var mapCompanyBenefitToViewModel = function (domainModel, companyGroupId) {
      var viewModel = {};

      viewModel['medical'] = domainModel.medical[0] != null;
      viewModel['dental'] = domainModel.dental[0] != null;
      viewModel['vision'] = domainModel.vision[0] != null;
      viewModel['hra'] = domainModel.hra[0] != null;
      viewModel['fsa'] = domainModel.fsa[0] != null;
      viewModel['supplemental_life'] = filterByCompanyGroup(domainModel.supplemental_life, companyGroupId);
      viewModel['std'] = domainModel.std[0] != null;
      viewModel['ltd'] = domainModel.ltd[0] != null;
      viewModel['basic_life'] = filterByCompanyGroup(domainModel.basic_life, companyGroupId);

      // TODO: update this logic to use Simon's refactored function
      viewModel['hsa'] = _.some(domainModel.hsa, function(plan) {
        return _.some(plan.company_groups, function(group) {
          return group.company_group.id == companyGroupId;
        });
      });

      return viewModel;
    };

    var getBenefitAvailabilityForUser = function(companyId, userId) {
      var deferred = $q.defer();

      UserService.getUserDataByUserId(userId).then(
        function(userData) {
          CompanyBenefitAvailabilityRepository.CompanyBenefitsByCompany.get({companyId: companyId})
          .$promise.then(function(benefits) {
            var viewCompanyBenefits = mapCompanyBenefitToViewModel(benefits, userData.companyGroupId);
            deferred.resolve(viewCompanyBenefits);
          }, function(error) {
            deferred.reject(error);
          });
        },
        function(errors) {
            deferred.reject(errors);
        }
      );

      return deferred.promise;
    };

    return{
      getBenefitAvailabilityForUser: getBenefitAvailabilityForUser
    };
}]);
