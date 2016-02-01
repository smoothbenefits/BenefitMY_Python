var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('PTOService',
  ['$q',
   'EnvironmentService',
   'PTORepository',
   function PTOService(
    $q,
    EnvironmentService,
    PTORepository){
        var _GetEnvAwareId = function(id){
            return EnvironmentService.getEnvironment().then(function(env){
                    return env + '_' + id;
                });
        };

        var GetPTOsByRequestor = function(requestor){
            return _GetEnvAwareId(requestor).then(function(id){
                return PTORepository.ByRequestor.query({userId:id})
                    .$promise.then(function(ptos){
                        return ptos;
                    });
                });
        };

        return {
            GetPTOsByRequestor: GetPTOsByRequestor
        };
    }
]);