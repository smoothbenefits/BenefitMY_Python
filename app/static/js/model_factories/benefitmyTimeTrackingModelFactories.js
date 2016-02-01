var benefitmyTimeTrackingModelFactories = angular.module('benefitmyTimeTrackingModelFactories', ['ngResource']);

benefitmyTimeTrackingModelFactories.factory('PTORepository', [
  '$resource',
  'TimeTrackingAppHostNameRepository',
  function ($resource, TimeTrackingAppHostNameRepository){
    return TimeTrackingAppHostNameRepository.get().$promise.then(function(response){
            var _hostName = response.hostname;
            return {
                ByRequestor: $resource(_hostName + 'api/v1/requestor/:userId/ptos', {userId:'@userId'}),
                ByApprover: $resource(_hostName + 'api/v1/approver/:userId/ptos', {userId:'@userId'}),
                Collection: $resource(_hostName + 'api/v1/ptos')
            };
    });
  }
]);

