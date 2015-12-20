var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('HsaService',
  ['$q', 'HsaRepository', 'PersonService',
  function ($q, HsaRepository, PersonService){

    var mapCompanyHsaPlanToDomainModel = function(viewModel) {
      return {
        "name": viewModel.planName,
        "company": viewModel.companyId
      };
    };

    var mapCompanyGroupHsaPlansToDomainModels = function(planId, groups) {
      var domainModelArray = [];
      _.each(groups, function(group) {
        domainModelArray.push({"company_group": group.id, "company_hsa_plan": planId});
      });

      return domainModelArray;
    };

    var getCompanyHsaPlanByCompany = function(companyId) {

    };

    var createHsaPlanForCompany = function(companyId, newPlan) {
      var groups = newPlan.selectedCompanyGroups;
      // First create an HSA plan for the company
      var companyPlanViewModel = mapCompanyHsaPlanToDomainModel(newPlan);
      return HsaRepository.ByCompany.save({companyId: companyId}, companyPlanViewModel)
      .$promise.then(function(response) {
        return response.id;
      }).then(function(companyPlanId) {
        // Get the company HSA plan id and assign to groups
        var domainModels = mapCompanyGroupHsaPlansToDomainModels(companyPlanId, groups);
        return HsaRepository.ByCompanyPlan.save({planId: companyPlanId}, domainModels)
        .$promise.then(function(response) {
          return response;
        });
      });
    };

    var updateCompanyHsaPlan = function(companyId, newPlan) {

    };

    var deleteCompanyHsaPlan = function(companyPlanId) {

    };

    var enrollHsaPlanForEmployee = function(employeeId, newPlan) {

    };

    var removeHsaPlanForEmployee = function(employeeId) {

    };

    var getHsaPlanByCompanyGroup = function(companyGroupId) {

    };

    return {
      GetCompanyHsaPlanByCompany: getCompanyHsaPlanByCompany,
      CreateHsaPlanForCompany: createHsaPlanForCompany,
      UpdateCompanyHsaPlan: updateCompanyHsaPlan,
      DeleteCompanyHsaPlan: deleteCompanyHsaPlan,
      EnrollHsaPlanForEmployee: enrollHsaPlanForEmployee,
      RemoveHsaPlanForEmployee: removeHsaPlanForEmployee,
      GetHsaPlanByCompanyGroup: getHsaPlanByCompanyGroup
    };
  }
]);
