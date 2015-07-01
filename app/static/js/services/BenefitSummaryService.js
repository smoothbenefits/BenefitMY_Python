var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitSummaryService',
  ['$q',
  'PersonService',
  'PersonBenefitEnrollmentRepository',
  'CompanyBenefitAvailabilityRepository',
  function BenefitSummaryService
    $q,
    PersonService,
    PersonBenefitEnrollmentRepository,
    CompanyBenefitAvailabilityRepository){

    var mapCompanyBenefitToViewModel = function(domainModel) {
      return null;
    };

    var mapPersonBenefitToViewModel = function (domainModel) {
      return null;
    };

    var getAvailableBenefitsByCompany = function(companyId){
      var deferred = $q.defer();

      CompanyBenefitAvailabilityRepository.CompanyBenefitsByCompany.get({companyId: companyId})
      .then(function(companyBenefits) {
        var viewCompanyBenefits = mapCompanyBenefitToViewModel(companyBenefits);
        deferred.resolve(viewCompanyBenefits);
      }, function (error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var getBenefitEnrollmentByUser = function(userId, companyId) {
      var deferred = $q.defer();

      PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
        var personId = personInfo.id;
        PersonBenefitEnrollmentRepository.BenefitEnrollmentByPerson.get({personId: personId})
        .then(function(enrollments) {
          var viewPersonBenefits = mapPersonBenefitToViewModel(enrollments);
          deferred.resolve(viewPersonBenefits);
        }, function(error) {
          deferred.reject(error);
        });
      });

      return deferred.promise;
    };

    return{
      getBenefitEnrollmentByUser: getBenefitEnrollmentByUser,
      getAvailableBenefitsByCompany: getAvailableBenefitsByCompany
    };
}]);
