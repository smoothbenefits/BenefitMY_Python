var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EnvironmentService',
    ['$q',
     '$http',
    function ($q, $http){
        return {
            isProd: function(){
                var deferred = $q.defer();
                $http({
                  method: 'GET',
                  url: '/api/v1/env'
                }).then(function(response){
                    deferred.resolve(response.data == 'PROD');
                }, function(error){
                    deferred.reject(error);
                });
                return deferred.promise;
            }
        };
    }
]);
