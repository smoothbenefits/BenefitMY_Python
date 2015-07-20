var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitPolicyKeyService',
  ['$http',
   '$q',
   'BenefitPolicyKeyRepository',
   function($http, $q, BenefitPolicyKeyRepository){
      var _benefitPolicyKeys = undefined;

      var getAllKeys = function(){
         var deferred = $q.defer();

         if(!_benefitPolicyKeys){
            BenefitPolicyKeyRepository.query().$promise.then(
                function(data) {
                   _benefitPolicyKeys = data;
                   deferred.resolve(_benefitPolicyKeys);
                },
                function(data){
                    deferred.reject(data);
                }
            )
         }
         else{
            deferred.resolve(_benefitPolicyKeys);
         }

         return deferred.promise;
      }

      return{
         getAllKeys: getAllKeys
      }
   }
]);
