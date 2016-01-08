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

      viewModel['medical'] = filterByCompanyGroup(domainModel.medical, companyGroupId);
      viewModel['dental'] = filterByCompanyGroup(domainModel.dental, companyGroupId);
      viewModel['vision'] = filterByCompanyGroup(domainModel.vision, companyGroupId);
      viewModel['hra'] = filterByCompanyGroup(domainModel.hra, companyGroupId);
      viewModel['fsa'] = filterByCompanyGroup(domainModel.fsa, companyGroupId);
      viewModel['supplemental_life'] = filterByCompanyGroup(domainModel.supplemental_life, companyGroupId);
      viewModel['std'] = filterByCompanyGroup(domainModel.std, companyGroupId);
      viewModel['ltd'] = filterByCompanyGroup(domainModel.ltd, companyGroupId);
      viewModel['basic_life'] = filterByCompanyGroup(domainModel.basic_life, companyGroupId);
      viewModel['hsa'] = filterByCompanyGroup(domainModel.hsa, companyGroupId);

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
