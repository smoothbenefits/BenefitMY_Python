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
        })
    };
  }
]);
