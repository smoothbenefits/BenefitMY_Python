var benefitmyDomainModelFactories = angular.module('benefitmyDomainModelFactories', ['ngResource']);

benefitmyDomainModelFactories.factory('currentUser', [
  '$resource',
  function ($resource){
    return $resource('/api/v1/users/current/', {})
  }
]);

benefitmyDomainModelFactories.factory('users', [
  '$resource',
  function ($resource){
    return $resource('/api/v1/users/:userId',
      {userId:'@Id'})
  }
]);

benefitmyDomainModelFactories.factory('userLogOut', [
     '$resource',
     function($resource){
      return $resource('/logout/', {})
     }]
);

benefitmyDomainModelFactories.factory('userSettingService',[
    '$resource',
    function($resource){
      return $resource('/api/v1/users/settings/');
}]);

benefitmyDomainModelFactories.factory('clientListRepository',[
    '$resource',
    function($resource){
        return $resource('/api/v1/users/:userId/company_roles/',
            {userId:'@id'})
}]);

benefitmyDomainModelFactories.factory('addClientRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies/', {})
    }]);

benefitmyDomainModelFactories.factory('companyRepository', [
  '$resource',
  function($resource){
    return $resource('/api/v1/companies/:clientId', {clientId:'@id'})
  }]);

benefitmyDomainModelFactories.factory('companyEmployeeBenefits', [
  '$resource',
  function($resource){
    return {
      selected:$resource('/api/v1/company_users/:companyId/benefits', {companyId: '@id'}),
      waived:$resource('/api/v1/companies/:companyId/waived_benefits', {companyId: '@id'})
    }
  }]);

benefitmyDomainModelFactories.factory('benefitListRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies/:clientId/benefits',
            {clientId:'@id'})
    }]);
benefitmyDomainModelFactories.factory('benefitDetailsRepository', [
    '$resource',
    function($resource){
      return $resource('/api/v1/benefit_details/plan=:planId/', {planId:'@id'});
    }]);

benefitmyDomainModelFactories.factory('benefitPlanRepository', [
    '$resource',
    function($resource){
        return {
          group:$resource('/api/v1/benefits/', {}),
          individual:$resource('/api/v1/benefits/:id', {id:'@id'})
        }
    }]);


benefitmyDomainModelFactories.factory('employerRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/companies/', {})
  }
]);

benefitmyDomainModelFactories.factory('employeeBenefits',
  ['$resource',
  function($resource){
    function enroll(){
      return $resource('/api/v1/users/:userId/benefits?company=:companyId', {userId: 'employee_id', companyId:'@company_id'});
    }

    function waive(){
      return $resource('/api/v1/users/:userId/waived_benefits', {userId: '@userid'});
    }

    return {
      enroll: enroll,
      waive: waive
    };
  }]);

benefitmyDomainModelFactories.factory('employerWorkerRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/companies/:companyId/users',
      {companyId:'@company_id'})
  }
]);
benefitmyDomainModelFactories.factory('usersRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/users/', {});
  }
]);

benefitmyDomainModelFactories.factory('employeeFamily', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/family/', {userId:'user_id'});
  }]);

benefitmyDomainModelFactories.factory('userDocument', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/documents/', {userId:'@userId'});
  }])

benefitmyDomainModelFactories.factory('documentRepository', ['$resource',
  function($resource){
    return {
      byUser: $resource('/api/v1/users/:userId/documents', {userId:'@user_id'}),
      type: $resource('/api/v1/document_types?company=:companyId', {companyId:'@company_id'}),
      create: $resource('/api/v1/documents/', {}),
      getById: $resource('/api/v1/documents/:id', {id:'@document_id'}),
      sign: $resource('/api/v1/documents/:id/signature', {id:'@document_id'}),
      updateById: $resource('/api/v1/documents/:id', {id: '@document_id'}, {'update': {method: 'PUT'}})
    };
  }
]);

benefitmyDomainModelFactories.factory('templateRepository', ['$resource',
  function($resource){
    return {
      update: $resource('/api/v1/templates/:id', {id: '@id'}, {
        'update': {method:'PUT'}
      }),
      create: $resource('/api/v1/templates/',{}),
      byCompany: $resource('/api/v1/companies/:companyId/templates/', {companyId:'@company_id'}),
      getById: $resource('/api/v1/templates/:id', {id:'@id'}),
      getAllFields: $resource('/api/v1/companies/:id/template_fields/', {id:'@id'})
    };
  }
]);

benefitmyDomainModelFactories.factory('employmentAuthRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/employment_authorization/', {userId: '@userId'});
  }]);

benefitmyDomainModelFactories.factory('employeeSignature', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/signature/', {userId: '@userId'});
  }]);

benefitmyDomainModelFactories.factory('countRepository', ['$resource',
  function($resource){
    return {
      employeeCount: $resource('/api/v1/company_employees_count/:companyId', {companyId: '@companyId'}),
      brokerCount: $resource('/api/v1/company_brokers_count/:companyId', {companyId: '@companyId'}),
      companyCount: $resource('/api/v1/broker_company_count/:brokerId', {brokerId: '@brokerId'})
    }
  }]);

benefitmyDomainModelFactories.factory('emailRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/onboard_email', {});
  }]);

benefitmyDomainModelFactories.factory('employeeTaxRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/w4/', {userId:'@userId'});
  }
]);
benefitmyDomainModelFactories.factory('peopleRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/people/:personId', {personId:'@personId'});
  }
]);

// FSA domain repo
benefitmyDomainModelFactories.factory('FsaPlanRepository', ['$resource', 
  function ($resource) {
    return $resource('/api/v1/broker/:id/fsa', {id: '@id'});
  }
]);

// FSA plan link to company
benefitmyDomainModelFactories.factory('CompanyFsaPlanRepository', ['$resource', 
  function ($resource) {
    return {
      ById: $resource('/api/v1/broker_company/:id/fsa', {id: '@id'}),
      ByCompany: $resource('/api/v1/company/:companyId/fsa', {companyId: '@companyId'})
    };
  }
]);

// Company FSA plan link to user
benefitmyDomainModelFactories.factory('FsaRepository', ['$resource',
  function ($resource){
    return {
      ByUser: $resource('/api/v1/user_company/:userId/fsa', {userId:'@user_id'}),
      ById: $resource('/api/v1/company_users/:id/fsa', {id:'@id'}, { 
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
      ByEmployeeId: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {post: { method: 'POST'}}),
      UpdateById: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {update: { method: 'PUT'}}),
      DeleteById: $resource('/api/v1/direct_deposit/:id', {id: '@id'}, {delete: { method: 'DELETE'}})
    };
  }
]);

benefitmyDomainModelFactories.factory('UploadRepository', ['$resource',
  function($resource){
    return {
      upload: $resource('/api/v1/upload/:pk/', {pk:'@pk'}),
      uploadsByUser: $resource('/api/v1/users/:pk/uploads/', {pk: '@pk'}),
      uploadsByCompany: $resource('/api/v1/companies/:compId/uploads/:pk', 
                                 {compId:'@compId', pk: '@pk'})
    };
  }
]);

benefitmyDomainModelFactories.factory('StdRepository', ['$resource',
  function($resource){
    return {
      PlanByUser: $resource('/api/v1/brokers/:userId/std_insurance_plan/', {userId:'@user_id'}),
      PlanById: $resource('/api/v1/brokers/:id/std_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      }),
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/std_insurance_plan/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company/:id/std_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      }),
      CompanyUserPlanByCompany: $resource('/api/v1/company_users/:companyId/std_insurance/', {companyId:'@company_id'}),
      CompanyUserPlanByUser: $resource('/api/v1/users/:userId/std_insurance/', {userId:'@user_id'}),
      CompanyUserPlanById: $resource('/api/v1/users/:id/std_insurance/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('LtdRepository', ['$resource',
  function($resource){
    return {
      PlanByUser: $resource('/api/v1/brokers/:userId/ltd_insurance_plan/', {userId:'@user_id'}),
      PlanById: $resource('/api/v1/brokers/:id/ltd_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      }),
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/ltd_insurance_plan/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company/:id/ltd_insurance_plan/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      }),
      CompanyUserPlanByCompany: $resource('/api/v1/company_users/:companyId/ltd_insurance/', {companyId:'@company_id'}),
      CompanyUserPlanByUser: $resource('/api/v1/users/:userId/ltd_insurance/', {userId:'@user_id'}),
      CompanyUserPlanById: $resource('/api/v1/users/:id/ltd_insurance/', {id:'@id'}, { 
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);