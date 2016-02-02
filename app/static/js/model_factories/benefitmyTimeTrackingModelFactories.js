var benefitmyTimeTrackingModelFactories = angular.module('benefitmyTimeTrackingModelFactories', ['ngResource']);

benefitmyTimeTrackingModelFactories.factory('TimeOffRepository', [
  '$resource',
  'TimeTrackingAppHostNameRepository',
  function ($resource, TimeTrackingAppHostNameRepository){
    return TimeTrackingAppHostNameRepository.get().$promise.then(function(response){
            var _hostName = response.hostname;
            return {
                ByRequestor: $resource(_hostName + 'api/v1/requestor/:userId/timeoffs', {userId:'@userId'}),
                ByApprover: $resource(_hostName + 'api/v1/approver/:userId/timeoffs', {userId:'@userId'}),
                Collection: $resource(_hostName + 'api/v1/timeoff')
            };
    });
  }
]);

