var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EnvironmentService',
    ['$q',
     'EnvironmentRepository',
    function ($q, EnvironmentRepository){
        return {
            isProd: function(){
                return EnvironmentRepository.get()
                      .$promise.then(function(response){
                            return response.env == 'PROD';
                      }, function(error){
                        deferred.reject(error);
                      });
            }
        };
    }
]);
