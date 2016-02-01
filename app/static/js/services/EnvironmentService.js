var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EnvironmentService',
    ['$q',
     'EnvironmentRepository',
    function ($q, EnvironmentRepository){
        var _cachedEnvironment;
        var getEnvironment = function(){
          if (!_cachedEnvironment)
          {
            return EnvironmentRepository.get()
                  .$promise.then(function(response){
                    _cachedEnvironment = response.env;
                    return _cachedEnvironment;
                  }); 
          }
          else{
            var deferred = $q.defer();
            deferred.resolve(_cachedEnvironment);
            return deferred.promise;
          }
        };

        var isProd = function(){
          return getEnvironment().then(function(environment){
            return environment == 'PROD';
          });
        };
        
        return {
            isProd: isProd,
            getEnvironment: getEnvironment
        };
    }
]);
