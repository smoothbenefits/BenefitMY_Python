var benefitmyDomainModelFactories = angular.module('benefitmyDomainModelFactories', ['ngResource']);

var PREFIX = '/api/v1/';

benefitmyDomainModelFactories.factory('EnvironmentRepository', [
  '$resource',
  function ($resource){
    return $resource(PREFIX + 'env/', {})
  }
]);

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

benefitmyDomainModelFactories.factory('companyRepository', [
  '$resource',
  function($resource){
    return $resource('/api/v1/companies/:clientId', {clientId:'@id'}, {
        'update': {method:'PUT'}
      })
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
          benefit:$resource('/api/v1/benefits/', {}),
          options:$resource('/api/v1/benefit_options', {}),
          individual:$resource('/api/v1/benefits/:id', {id:'@id'})
        }
    }]);

benefitmyDomainModelFactories.factory('CompanyGroupHealthBenefitsPlanOptionRepository', ['$resource',
  function($resource){
    return{
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/health_benefits/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_health_benefits/:companyPlanId/company_group_plans/', {companyPlanId:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

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

benefitmyDomainModelFactories.factory('documentRepository', ['$resource',
  function($resource){
    return {
      byUser: $resource('/api/v1/users/:userId/documents', {userId:'@user_id'}),
      type: $resource('/api/v1/document_types?company=:companyId', {companyId:'@company_id'}),
      create: $resource('/api/v1/documents/', {}),
      getById: $resource('/api/v1/documents/:id', {id:'@document_id'}),
      sign: $resource('/api/v1/documents/:id/signature', {id:'@document_id'}),
      updateById: $resource('/api/v1/documents/:id', {id: '@document_id'}, {'update': {method: 'PUT'}}),
      byCompany: $resource('/api/v1/companies/:companyId/documents', {companyId:'@company_id'}, {'save': {method:'POST', isArray: true}})
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

benefitmyDomainModelFactories.factory('SignatureRepository', ['$resource',
  function($resource){
    return {
      ById: $resource(PREFIX + 'signature/:signatureId/', {signatureId: '@signatureId'}),
      ByUser: $resource(PREFIX + 'users/:userId/signature/', {userId: '@userId'})
    }
  }
]);

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
    return {
        ById: $resource('/api/v1/people/:personId', {personId:'@personId'}, {update: {method: 'PUT'}}),
        ByUser: $resource('/api/v1/users/:userId/family', {userId:'@userId'})
    };
  }
]);

// FSA domain repo
benefitmyDomainModelFactories.factory('FsaPlanRepository', ['$resource',
  function ($resource) {
    return $resource('/api/v1/brokers/:id/fsa', {id: '@id'});
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

benefitmyDomainModelFactories.factory('CompanyGroupFsaPlanRepository', ['$resource',
  function($resource){
    return{
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/company_fsa/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_fsa/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
          method:'POST',
          isArray: true
        },
        update: {
          method: 'PUT',
          isArray: true
        }
      })
    };
  }
]);

// Life insurance plan domain repo
benefitmyDomainModelFactories.factory('BasicLifeInsurancePlanRepository', ['$resource',
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
benefitmyDomainModelFactories.factory('CompanyBasicLifeInsurancePlanRepository', ['$resource',
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

benefitmyDomainModelFactories.factory('CompanyGroupBasicLifeInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/basic_life_insurance_plan/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_basic_life_insurance_plan/:companyPlanId/company_group_plans/', {companyPlanId:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

// Company life insurance plan to users link domain repo
benefitmyDomainModelFactories.factory('CompanyUserBasicLifeInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompany: $resource('/api/v1/company_users/:companyId/life_insurance/', {companyId:'@company_id'}),
      ByUser: $resource('/api/v1/users/:userId/life_insurance/', {userId:'@user_id'}),
      ById: $resource('/api/v1/users/:id/life_insurance/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      PlanPremiumByUser: $resource('/api/v1/user/:userId/life_insurance_plan/:planId/premium/', {userId: '@userId', planId: '@planId'})
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
                                 {compId:'@compId', pk: '@pk'}),
      uploadApplicationFeature: $resource('/api/v1/upload/application_features/:app_feature/:feature_id',
                                          {app_feature:'@app_feature', feature_id:'@feature_id'})
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
      CompanyPlanPremiumByUser: $resource('/api/v1/user/:userId/std_insurance/:id/premium/',
        {userId: '@user_id', id: '@id'}),
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

benefitmyDomainModelFactories.factory('CompanyGroupStdInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/std_insurance/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/std_insurance/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
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
      CompanyPlanPremiumByUser: $resource('/api/v1/user/:userId/ltd_insurance/:id/premium/',
        {userId:'@user_id', id:'@id'}),
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

benefitmyDomainModelFactories.factory('CompanyGroupLtdInsurancePlanRepository', ['$resource',
  function ($resource){
    return {
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/ltd_insurance/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/ltd_insurance/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('EmployeeProfileRepository', ['$resource',
  function($resource){
    return {
      ByPersonCompany: $resource('/api/v1/person/:personId/company/:companyId/employee_profile', {personId:'@personId', companyId:'@companyId'}),
      ByCompanyUser: $resource('/api/v1/company/:companyId/user/:userId/employee_profile', {userId:'@userId', companyId:'@companyId'}),
      ById: $resource('/api/v1/employee_profile/:id', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      ByCompany: $resource('/api/v1/company/:companyId/employee_profiles', {companyId: '@companyId'})
    };
  }
]);

benefitmyDomainModelFactories.factory('SupplementalLifeInsuranceRepository', ['$resource',
  function($resource){
    return {
      PlanById: $resource('/api/v1/supplemental_life/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/company_suppl_life/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company_suppl_life/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPersonPlanByCompany: $resource('/api/v1/company/:companyId/person_comp_suppl_life/', {companyId:'@company_id'}),
      CompanyPersonPlanByPerson: $resource('/api/v1/person/:personId/person_comp_suppl_life/', {personId:'@person_id'}),
      CompanyPersonPlanById: $resource('/api/v1/person_comp_suppl_life/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyGroupSupplLifeInsurancePlanRepository', ['$resource',
  function($resource){
    return{
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/company_suppl_life/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_suppl_life/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('HraRepository', ['$resource',
  function($resource){
    return {
      PlanById: $resource('/api/v1/hra_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/company_hra_plan/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company_hra_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPersonPlanByPerson: $resource('/api/v1/person/:personId/person_company_hra_plan/', {personId:'@person_id'}),
      CompanyPersonPlanById: $resource('/api/v1/person_company_hra_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyGroupHraPlanRepository', ['$resource',
  function($resource){
    return{
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/company_hra/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_hra/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('CommuterRepository', ['$resource',
  function($resource){
    return {
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/company_commuter_plan/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company_commuter_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPersonPlanByPerson: $resource('/api/v1/person/:personId/person_company_commuter_plan/', {personId:'@person_id'}),
      CompanyPersonPlanById: $resource('/api/v1/person_company_commuter_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyGroupCommuterPlanRepository', ['$resource',
  function($resource){
    return{
      ByCompanyGroup: $resource('/api/v1/company_group/:companyGroupId/company_commuter/', {companyGroupId:'@company_group_id'}),
      ByCompanyPlan: $resource('/api/v1/company_commuter/:pk/company_group_plans/', {pk:'@pk'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('ExtraBenefitRepository', ['$resource',
  function($resource){
    return {
      CompanyPlanByCompany: $resource('/api/v1/company/:companyId/company_extra_benefit_plan/', {companyId:'@company_id'}),
      CompanyPlanById: $resource('/api/v1/company_extra_benefit_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      }),
      CompanyPersonPlanByPerson: $resource('/api/v1/person/:personId/person_company_extra_benefit_plan/', {personId:'@person_id'}),
      CompanyPersonPlanById: $resource('/api/v1/person_company_extra_benefit_plan/:id/', {id:'@id'}, {
        update: {
            method: 'PUT'
        }
      })
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyBenefitAvailabilityRepository', ['$resource',
  function ($resource) {
    return {
      CompanyBenefitsByCompany: $resource(PREFIX + 'company/:companyId/benefits', {companyId: '@companyId'})
    };
  }
]);

benefitmyDomainModelFactories.factory('PersonBenefitEnrollmentRepository', ['$resource',
  function ($resource) {
    return {
      BenefitEnrollmentByPerson: $resource(PREFIX + 'person/:personId/benefits', {personId: '@personId'})
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyFeatureRepository', ['$resource',
  function($resource) {
    return {
      AllApplicationFeatureStatusByCompany: $resource(PREFIX + 'all_company_features/:companyId/', {companyId: '@company_id'}),
    };
  }
]);

benefitmyDomainModelFactories.factory('BenefitPolicyKeyRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/benefit_policy_keys');
  }
]);

benefitmyDomainModelFactories.factory('PeriodDefinitionRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/period_definitions');
  }
]);

benefitmyDomainModelFactories.factory('CompensationRepository', ['$resource',
  function($resource){
    return {
      ByCompensationId: $resource(PREFIX + 'employee_compensation/:id/', {id: '@id'}),
      ByPersonId: $resource(PREFIX + 'person/:personId/employee_compensation', {personId: '@personId'})
    };
  }
]);

benefitmyDomainModelFactories.factory('CompanyEmployeeEnrollmentSummaryRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:comp_id/enrollment_summary', {comp_id:'@comp_id'})
    };
  }
]);

benefitmyDomainModelFactories.factory('BatchAccountCreationDataParseRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:company_id/batch_account_creation/parse_account_data/', {company_id:'@company_id'})
    };
  }
]);

benefitmyDomainModelFactories.factory('BatchAccountCreationBatchCreateRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:company_id/batch_account_creation/batch_create/', {company_id:'@company_id'})
    }
  }
]);

benefitmyDomainModelFactories.factory('BatchEmployeeOrganizationImportDataParseRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:company_id/batch_employee_organization_import/parse_organization_data/', {company_id:'@company_id'})
    };
  }
]);

benefitmyDomainModelFactories.factory('BatchEmployeeOrganizationImportRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:company_id/batch_employee_organization_import/batch_import/', {company_id:'@company_id'})
    }
  }
]);

benefitmyDomainModelFactories.factory('EmployeeManagementEmployeeTerminationRepository', ['$resource',
  function($resource){
    return{
      ByCompany:$resource(PREFIX + 'company/:company_id/employee_management/termination/', {company_id:'@company_id'})
    }
  }
]);

benefitmyDomainModelFactories.factory('Company1095CDataRepository', ['$resource',
  function($resource){
    return {
      ByCompany: $resource(PREFIX + 'companies/:comp_id/1095_c', {comp_id:'@comp_id'}),
      Periods: $resource(PREFIX + '1095_c_periods')
    }
  }
]);

benefitmyDomainModelFactories.factory('Company1094CDataRepository', ['$resource',
  function($resource) {
    return {
      ByCompany: $resource(PREFIX + 'companies/:comp_id/1094_c', {comp_id: '@comp_id'}),
      EligibilityCertification: $resource(PREFIX + '1094_c_certificiations')
    }
  }
]);

benefitmyDomainModelFactories.factory('Employee1095CDataRepository', ['$resource',
  function($resource){
    return {
      ByPersonCompany: $resource(PREFIX + 'company/:companyId/person/:personId/1095_c',
                        {companyId: '@companyId', personId: '@personId'})
    }
  }
]);

benefitmyDomainModelFactories.factory('CompanyUserDetailRepository', ['$resource',
  function($resource){
    return {
      ByCompany: $resource(PREFIX + 'company/:comp_id/role/:role', {comp_id:'@comp_id', role:'@role'})
    }
  }
]);

benefitmyDomainModelFactories.factory('CompanyGroupRepository', ['$resource',
  function($resource) {
    return {
      ByCompany: $resource(PREFIX + 'company/:companyId/groups', {companyId: '@companyId'}),
      ById: $resource(PREFIX + 'company_group/:groupId', {groupId: '@groupId'}, {
        update: { method: 'PUT' }
      })
    }
  }
]);

benefitmyDomainModelFactories.factory('CompanyGroupMemberRepository', ['$resource',
  function($resource) {
    return {
      ByCompany: $resource(PREFIX + 'company/:companyId/group_member', {companyId: '@companyId'}),
      ByCompanyGroup: $resource(PREFIX + 'company_group/:groupId/members', {groupId: '@groupId'}),
      ById: $resource(PREFIX + 'company_group_member/:groupMemberId', {groupMemberId: '@groupMemberId'}, {
        update: { method: 'PUT' }
      })
    }
  }
]);

benefitmyDomainModelFactories.factory('HsaRepository', ['$resource',
  function($resource) {
    return {
      ByCompany: $resource(PREFIX + 'company/:companyId/hsa', {companyId: '@companyId'}),
      ByCompanyPlan: $resource(PREFIX + 'company/hsa/:planId', {planId: '@planId'}),
      ByCompanyGroup: $resource(PREFIX + 'company_group/:groupId/hsa', {groupId: '@groupId'}),
      GroupPlanByCompanyPlan: $resource(PREFIX + 'company_hsa_plan/:planId/company_group_plans', {planId: '@planId'}, {
        save: {
            method:'POST',
            isArray: true
        },
        update: {
            method: 'PUT',
            isArray: true
        }
      }),
      ByPerson: $resource(PREFIX + 'person/:personId/hsa', {personId: '@personId'}),
      ByPersonPlan: $resource(PREFIX + 'person_hsa/:personPlanId/hsa', {personPlanId: '@personPlanId'}, {
        update: { method: 'PUT' }
      })
    };
  }
]);


benefitmyDomainModelFactories.factory('UserOnboardingStepStateRepository', ['$resource',
  function($resource) {
    return {
      ByUser: $resource(PREFIX + 'users/:userId/onboarding_step_states', {userId: '@userId'}),
      ById: $resource(PREFIX + 'onboarding_step_states/:entryId', {entryId: '@entryId'}, {
        update: { method: 'PUT' }
      })
    }
  }
]);

benefitmyDomainModelFactories.factory('CompanyServiceProviderRepository', ['$resource',
  function($resource) {
    return {
      ByCompany: $resource(PREFIX + 'company/:companyId/company_service_providers', {companyId: '@companyId'}),
      ById: $resource(PREFIX + 'company_service_provider/:entryId', {entryId: '@entryId'}, {
        update: { method: 'PUT' }
      })
    }
  }
]);

benefitmyDomainModelFactories.factory('PhraseologyRepository', ['$resource',
  function($resource) {
    return {
      All: $resource(PREFIX + 'phraseologys'),
      CompanyPhraseologyById: $resource(PREFIX + 'company_phraseologys/:id', {id: '@id'}, {
        update: { method: 'PUT' }
      }),
      CompanyPhraseologysByCompany: $resource(PREFIX + 'company/:companyId/phraseologys', {companyId: '@companyId'}),
      EmployeePhraseologyById: $resource(PREFIX + 'employee_phraseologys/:id', {id: '@id'}, {
        update: { method: 'PUT' }
      }), 
      EmployeePhraseologysByPerson: $resource(PREFIX + 'person/:personId/phraseologys', {personId: '@personId'})
    }
  }
]);
