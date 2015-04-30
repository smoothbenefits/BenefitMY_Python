var benefitmyService = angular.module('benefitmyService');
benefitmyService.factory('ApplicationFeatureService',
  ['$http',
   '$q',
   function($http, $q){
      var _cached = false;
      var _applicationFeatures = {};
      var getAppFeature = function(){
         var deferred = $q.defer();
         $http.get('/api/v1/application_features/').success(function(data){
            _.each(data, function(item){
               _applicationFeatures[item.feature] = item.id;
            });
            _cached = true;
            deferred.resolve(_applicationFeatures);
         }).error(function(data){
            deferred.reject(data);
         });
         return deferred.promise;
      }
      return{
         isApplicationFeatureCached: _cached,
         getFromServer: getAppFeature,
         cachedApplicationFeatures: _applicationFeatures
      }
   }
]);