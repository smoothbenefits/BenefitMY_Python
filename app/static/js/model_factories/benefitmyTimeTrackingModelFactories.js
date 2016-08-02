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
            }),
            QuotaByUser: $resource(_hostName + 'api/v1/person/:userId/timeoff_quota', {userId:'@userId'}, {
                update: { method: 'PUT' }
            }),
            QuotaByCompany: $resource(_hostName + 'api/v1/company/:companyId/timeoff_quotas', {companyId:'@companyId'})
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
            Collection: $resource(_hostName + 'api/v1/work_timesheets'),
            ById: $resource(_hostName + 'api/v1/work_timesheets/:id', {id:'@id'}, {
              update: { method: 'PUT' }
            }),
            ByCompany: $resource(_hostName + 'api/v1/company/:companyId/work_timesheets', {companyId: '@companyId'}),
            RecordTypes: $resource(_hostName + 'api/v1/work_timesheets/record_types')
        };
  }
]);

benefitmyTimeTrackingModelFactories.factory('TimePunchCardRepository', [
  '$resource',
  'envService',
  function ($resource, envService){
    var _hostName = envService.read('timeTrackingUrl');
    return {
      ByEmployee: $resource(_hostName + 'api/v1/employee/:id/time_punch_cards', {id:'@id'}),
      Collection: $resource(_hostName + 'api/v1/time_punch_cards', {}, {
        save: { method: 'POST', isArray: true }
      }),
      ById: $resource(_hostName + 'api/v1/time_punch_cards/:id', {id:'@id'}, {
        update: { method: 'PUT' }
      }),
      ByCompany: $resource(_hostName + 'api/v1/company/:id/time_punch_cards', {companyId: '@id'})
    };
  }
]);
