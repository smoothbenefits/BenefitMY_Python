var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyBenefitEnrollmentSummaryService',
  ['$q',
   'CompanyEmployeeEnrollmentSummaryRepository',
   function (
        $q,
        CompanyEmployeeEnrollmentSummaryRepository){

        var getEnrollmentSummary = function(companyId){
            var deferred = $q.defer();
            CompanyEmployeeEnrollmentSummaryRepository.ByCompany.get({comp_id:companyId})
            .$promise.then(function(response){
              deferred.resolve({notStarted: response.enrollmentNotStarted,
                                notComplete: response.enrollmentNotComplete,
                                completed: response.enrollmentCompleted,
                                total: response.totalEmployeeCount});
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            return deferred.promise;
        };

        return {
            getEnrollmentSummary: getEnrollmentSummary
        };
   }
]);