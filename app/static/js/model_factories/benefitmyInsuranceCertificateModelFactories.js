var benefitmyInsuranceCertificateModelFactories = angular.module('benefitmyInsuranceCertificateModelFactories', ['ngResource']);

benefitmyInsuranceCertificateModelFactories.factory('ContractorsRepository', [
  '$resource',
  'envService',
  function ($resource, envService){
    var _hostName = envService.read('insuranceCertificateUrl');
    return {
        ByCompany: $resource(_hostName + 'api/v1/company/:compId/contractors', {compId:'@compId'}),
        ById: $resource(_hostName + 'api/v1/contractor/:contractorId', {contractorId:'@contractorId'}, {
          update: { method: 'PUT' }
        }),
        Collection: $resource(_hostName + 'api/v1/contractors'),
        StatusById: $resource(_hostName + 'api/v1/contractor/:contractorId/status', {contractorId:'@contractorId'}, {
          update: { method: 'PUT' }
        }),
        InsuranceCertificates: $resource(_hostName + 'api/v1/contractor/:contractorId/insurance',
          {
            contractorId: '@contractorId'
          }
        ),
        InsuranceCertificateById: $resource(_hostName + 'api/v1/contractor/:contractorId/insurance/:insuranceCertificateId',
          {
            contractorId: '@contractorId',
            insuranceCertificateId: '@insuranceCertificateId'
          }
        )
    };
  }
]);

benefitmyInsuranceCertificateModelFactories.factory('ProjectRepository', [
  '$resource',
  'envService',
  function ($resource, envService){
    var _hostName = envService.read('insuranceCertificateUrl');
    return {
        ByCompany: $resource(_hostName + 'api/v1/company/:compId/projects', {compId:'@compId'}),
        ById: $resource(_hostName + 'api/v1/project/:projectId', {projectId:'@projectId'}, {
          update: { method: 'PUT' }
        }),
        Collection: $resource(_hostName + 'api/v1/project'),
        StatusById: $resource(_hostName + 'api/v1/project/:projectId/status', {projectId:'@projectId'}, {
          update: { method: 'PUT' }
        }),
        PayableByProjectId: $resource(_hostName + 'api/v1/project/:projectId/payable', {projectId: '@projectId'}),
        PayableByProjectPayable: $resource(_hostName + 'api/v1/project/:projectId/payable/:payableId',
          {projectId: '@projectId', payableId: '@payableId'})
    };
  }
]);
