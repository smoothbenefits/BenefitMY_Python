var benefitmyTimeTrackingModelFactories = angular.module('benefitmyTimeTrackingModelFactories', ['ngResource']);

benefitmyTimeTrackingModelFactories.factory('PTORepository', [
  '$resource',
  function ($resource){
    return {
        ByRequestor: $resource('localhost:6999/api/v1/requestor/:userId/ptos', {userId:'@userId'}),
        ByApprover: $resource('localhost:6999/api/v1/approver/:userId/ptos', {userId:'@userId'}),
        Collection: $resource('localhost:6999/api/v1/ptos')
    }
  }
]);

