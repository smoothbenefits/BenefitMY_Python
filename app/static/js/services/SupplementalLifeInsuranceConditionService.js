var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('SupplementalLifeInsuranceConditionService',
  ['$http',
   '$q',
   function($http, $q){
      var _conditions = undefined;

      var getConditions = function(){
         var deferred = $q.defer();

         if(!_conditions){
            $http.get('/api/v1/supplemental_life_condition/').success(function(data){
               _conditions = {};
               _.each(data, function(item){
                  _conditions[item.name] = item;
               });
               deferred.resolve(_conditions);
            }).error(function(data){
               deferred.reject(data);
            });
         }
         else{
            deferred.resolve(_conditions);
         }
         return deferred.promise;
      }
      return{
         getConditions: getConditions
      }
   }
]);