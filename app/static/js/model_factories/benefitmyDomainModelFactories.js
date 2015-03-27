var benefitmyDomainModelFactories = angular.module('benefitmyDomainModelFactories', ['ngResource']);

// FSA domain repo
benefitmyDomainModelFactories.factory('FsaRepository', ['$resource',
  function ($resource){
    return {
      ByUser: $resource('/api/v1/fsa/:userId', {userId:'@user_id'}),
      ById: $resource('/api/v1/fsa/:id', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

// Life insurance plan domain repo
benefitmyDomainModelFactories.factory('LifeInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByUser: $resource('/api/v1/brokers/:userId/life_insurance_plan/', {userId:'@user_id'}),
      ById: $resource('/api/v1/brokers/:id/life_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

// Life insurance plan to company link domain repo
benefitmyDomainModelFactories.factory('CompanyLifeInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompany: $resource('/api/v1/company/:companyId/life_insurance_plan/', {companyId:'@company_id'}),
      ById: $resource('/api/v1/company/:id/life_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

// Company life insurance plan to users link domain repo
benefitmyDomainModelFactories.factory('CompanyUserLifeInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompany: $resource('/api/v1/company_users/:companyId/life_insurance/', {companyId:'@company_id'}),
      ByUser: $resource('/api/v1/users/:userId/life_insurance/', {userId:'@user_id'}),
      ById: $resource('/api/v1/users/:id/life_insurance/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

// Direct deposit domain repo
benefitmyDomainModelFactories.factory('DirectDepositRepository', ['$resource',
  function($resource){
    return {
      ByEmployeeId: $resource('/api/v1/direct_deposit/:id', {id: '@id'}),
      UpdateByEmployeeId: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {update: { method: 'PUT'}}),
      CreateByEmployeeId: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {post: { method: 'POST', isArray: true}}),
      DeleteById: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {delete: { method: 'DELETE'}})
    };
  }
]);
