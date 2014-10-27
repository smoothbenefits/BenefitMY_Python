var benefitmyService = angular.module('benefitmyService', ['ngResource']);

benefitmyService.factory('currentUser', [
	'$resource',
	function ($resource){
		return $resource('/api/v1/users/current', {})
	}
]);

benefitmyService.factory('users', [
	'$resource',
	function ($resource){
		return $resource('/api/v1/users/:userId',
			{userId:'@Id'})
	}
]);

benefitmyService.factory('userLogOut', [
     '$resource',
     function($resource){
     	return $resource('api/v1/users/sign_out', {})
     }]
);

benefitmyService.factory('clientListRepository',[
    '$resource',
    function($resource){
        return $resource('/api/v1/users/:userId/company_roles',
            {userId:'@id'})
}]);

benefitmyService.factory('addClientRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies', {})
    }]);

benefitmyService.factory('companyRepository', [
  '$resource',
  function($resource){
    return $resource('/api/v1/companies/:clientId', {clientId:'@id'})
  }]);

benefitmyService.factory('benefitListRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies/:clientId/benefits',
            {clientId:'@id'})
    }]);

benefitmyService.factory('addBenefitRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/benefits', {})
    }]);


benefitmyService.factory('employerRepository', ['$resource',
  function($resource){
  	return $resource('/api/v1/companies', {})
  }
]);

benefitmyService.factory('employeeCompanyRoles', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/company_roles', {userId: '@id'})
  }]);

benefitmyService.factory('employeeBenefits', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/benefits?company=:companyId', {userId: 'employee_id', companyId:'@company_id'})
  }]);

benefitmyService.factory('employerWorkerRepository', ['$resource',
  function($resource){
  	return $resource('/api/v1/companies/:companyId/users',
  		{companyId:'@company_id'})
  }
]);
benefitmyService.factory('usersRepository', ['$resource',
  function($resource){
  	return $resource('api/v1/users', {});
  }
]);

benefitmyService.factory('employeeFamily', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/family', {userId:'user_id'});
  }]);

benefitmyService.factory('documentRepository', ['$resource',
  function($resource){
    return {
      byUser: $resource('/api/v1/users/:userId/documents?company=:companyId', {userId:'@user_id', companyId:'@company_id'}),
      type: $resource('/api/v1/document_types?company=:companyId', {companyId:'@company_id'}),
      create: $resource('/api/v1/documents', {}),
      getById: $resource('/api/v1/documents/:id', {id:'@document_id'})
    };
  }
]);

benefitmyService.factory('templateRepository', ['$resource',
  function($resource){
    return {
      create: $resource('/api/v1/templates',{}),
      byCompany: $resource('/api/v1/companies/:companyId/templates', {companyId:'@company_id'}),
      getById: $resource('/api/v1/templates/:id', {id:'@id'})
    };
  }
                         ]);
