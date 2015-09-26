var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyBenefitAvailabilityService',
  ['$q',
  'CompanyBenefitAvailabilityRepository',
  function BenefitSummaryService(
    $q,
    CompanyBenefitAvailabilityRepository){
    var FullTimeBenefitFlag

    var mapCompanyBenefitToViewModel = function (domainModel) {
      var viewModel = {};

      viewModel['medical'] = domainModel.medical[0] != null;
      viewModel['dental'] = domainModel.dental[0] != null;
      viewModel['vision'] = domainModel.vision[0] != null;
      viewModel['hra'] = domainModel.hra[0] != null;
      viewModel['fsa'] = domainModel.fsa[0] != null;
      viewModel['basic_life'] = domainModel.basic_life[0] != null;
      viewModel['supplemental_life'] = domainModel.supplemental_life[0] != null;
      viewModel['std'] = domainModel.std[0] != null;
      viewModel['ltd'] = domainModel.ltd[0] != null;

      return viewModel;
    };

    var getBenefitAvailabilityByCompany = function(companyId) {
      var deferred = $q.defer();

      CompanyBenefitAvailabilityRepository.CompanyBenefitsByCompany.get({companyId: companyId})
      .$promise.then(function(benefits) {   
        var viewCompanyBenefits = mapCompanyBenefitToViewModel(benefits);
        deferred.resolve(viewCompanyBenefits);
      }, function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    return{
      getBenefitAvailabilityByCompany: getBenefitAvailabilityByCompany
    };
}]);
