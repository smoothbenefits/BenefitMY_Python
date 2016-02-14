var benefitmyTimeTrackingModelFactories = angular.module('benefitmyTimeTrackingModelFactories', ['ngResource']);

benefitmyTimeTrackingModelFactories.factory('TimeOffRepository', [
  '$resource',
  'envService',
  function ($resource, envService){
        var _hostName = envService.read('timeTrackingUrl');
        return {
            ByRequestor: $resource(_hostName + 'api/v1/requestor/:userId/timeoffs', {userId:'@userId'}),
            ByApprover: $resource(_hostName + 'api/v1/approver/:userId/timeoffs', {userId:'@userId'}),
            Collection: $resource(_hostName + 'api/v1/timeoffs'),
            StatusByTimeoffId: $resource(_hostName + 'api/v1/timeoffs/:timeoffId/status', {timeoffId:'@id'}, {
              update: { method: 'PUT' }
            })
        };
  }
]);

benefitmyTimeTrackingModelFactories.factory('WorkTimesheetRepository', [
  '$resource',
  'envService',
  function ($resource, envService){
        var _hostName = envService.read('timeTrackingUrl');
        return {
            ByEmployee: $resource(_hostName + 'api/v1/employee/:userId/work_timesheets', {userId:'@userId'}),
            Collection: $resource(_hostName + 'api/v1/work_timesheets')
        };
  }
]);

