var benefitmyService = angular.module('benefitmyService');
benefitmyService.factory('ApplicationFeatureService',
  ['$http',
   '$q',
   function($http, $q){
      var _applicationFeatures = undefined;

      var getAppFeature = function(){
         var deferred = $q.defer();

         if(!_applicationFeatures){
            $http.get('/api/v1/application_features/').then(
                function(response){
                   _applicationFeatures = {};
                   _.each(response.data, function(item){
                      _applicationFeatures[item.feature] = item.id;
                   });
                   deferred.resolve(_applicationFeatures);
                },
                function(response){
                   deferred.reject(response);
                }
            );
         }
         else{
            deferred.resolve(_applicationFeatures);
         }
         return deferred.promise;
      }
      return{
         getApplicationFeatures: getAppFeature
      }
   }
]);
