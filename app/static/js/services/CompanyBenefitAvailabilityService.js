var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyBenefitAvailabilityService',
  ['$q',
  'CompanyBenefitAvailabilityRepository',
  'UserService',
  function BenefitSummaryService(
    $q,
    CompanyBenefitAvailabilityRepository,
    UserService){

    var mapCompanyBenefitToViewModel = function (domainModel, companyGroupId) {
      var viewModel = {};

      viewModel['medical'] = domainModel.medical[0] != null;
      viewModel['dental'] = domainModel.dental[0] != null;
      viewModel['vision'] = domainModel.vision[0] != null;
      viewModel['hra'] = domainModel.hra[0] != null;
      viewModel['fsa'] = domainModel.fsa[0] != null;
      viewModel['supplemental_life'] = domainModel.supplemental_life[0] != null;
      viewModel['std'] = domainModel.std[0] != null;
      viewModel['ltd'] = domainModel.ltd[0] != null;
      viewModel['basic_life'] = _.some(domainModel.basic_life,
        function(plan) {
            return _.some(plan.company_groups, function(company_group) {
                return company_group.company_group.id == companyGroupId;
            });
        });

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
            if(userData.user.company_group_user[0]) {
              var viewCompanyBenefits = mapCompanyBenefitToViewModel(benefits, userData.user.company_group_user[0].company_group.id);
              deferred.resolve(viewCompanyBenefits);
            } else {
              deferred.resolve({});
            }
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
