var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitUpdateReasonService',
  ['$http',
   '$q',
   function($http, $q){
      var _benefitUpdateReasons = undefined;

      var getAllReasons = function(){
         var deferred = $q.defer();

         if(!_benefitUpdateReasons){
            $http.get('/api/v1/benefit_update_reasons/').success(function(data){
               _benefitUpdateReasons = [];
               _.each(data, function(item){
                  _benefitUpdateReasons.push(item);
               });
               deferred.resolve(_benefitUpdateReasons);
            }).error(function(data){
               deferred.reject(data);
            });
         }
         else{
            deferred.resolve(_benefitUpdateReasons);
         }
         return deferred.promise;
      }

      return{
         getAllReasons: getAllReasons
      }
   }
]);