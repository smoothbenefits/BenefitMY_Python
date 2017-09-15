var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('SupplementalLifeInsuranceConditionService',
  ['$http',
   '$q',
   function($http, $q){
      var _conditions = undefined;

      var mapConditionDomainToViewModel = function(conditionDomainModel) {
            var viewModel = {};

            viewModel.conditionId = conditionDomainModel.id;
            viewModel.name = conditionDomainModel.name;
            viewModel.description = conditionDomainModel.description;

            return viewModel;
        };

      var getConditions = function(){
         var deferred = $q.defer();

         if(!_conditions){
            $http.get('/api/v1/supplemental_life_condition/').then(
                function(response){
                   _conditions = {};
                   _.each(response.data, function(item){
                      _conditions[item.name] = mapConditionDomainToViewModel(item);
                   });
                   deferred.resolve(_conditions);
                },
                function(response){
                   deferred.reject(response);
                }
            );
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
