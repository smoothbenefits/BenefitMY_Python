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

    var mapCompanyHsaPlansToViewModels = function(domainModels) {
      var companyPlans = [];
      _.each(domainModels, function(plan) {
        var viewModel = {
          "hsaPlanName": plan.name,
          "companyPlanId": plan.id,
          "groups": plan.company_groups
        };
        companyPlans.push(viewModel);
      });

      return companyPlans;
    };

    var getCompanyHsaPlanByCompany = function(companyId) {
      return HsaRepository.ByCompany.query({companyId: companyId}).$promise
      .then(function(companyPlans) {
        var hsaViewModels = mapCompanyHsaPlansToViewModels(companyPlans);
        return hsaViewModels;
      });
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
        return HsaRepository.GroupPlanByCompanyPlan.save({planId: companyPlanId}, domainModels)
        .$promise.then(function(response) {
          return response;
        });
      });
    };

    var deleteCompanyHsaPlan = function(companyPlanId) {
      return HsaRepository.ByCompanyPlan.delete({planId: companyPlanId}).$promise
      .then(function(response) {
        return response;
      });
    };

    var mapPersonHsaPlanToViewModel = function(domainModel) {
      var viewModel = angular.copy(domainModel);
      if (domainModel && domainModel.amount_per_year) {
        viewModel.electedAmount = parseInt(domainModel.amount_per_year);
      } else {
        viewModel.electedAmount = 0;
      }
      return viewModel;
    }

    var getHsaPlanEnrollmentByUser = function(employeeUserId) {
      return PersonService.getSelfPersonInfo(employeeUserId).then(function(person) {
        return person.id;
      }).then(function(personId) {
        return HsaRepository.ByPerson.query({personId: personId}).$promise
        .then(function(response) {
          var mapped = mapPersonHsaPlanToViewModel(response);
          return mapped;
        });
      });
    };

    var enrollHsaPlanForEmployee = function(employeeId, newPlan) {

    };

    var removeHsaPlanForEmployee = function(employeeId) {

    };

    var mapCompanyGroupHsaPlansToViewModels = function(domainModels) {
      var viewModels = [];
      _.each(domainModels, function(model) {
        var viewModel = {
          "hsaPlanName": model.company_hsa_plan.name,
          "group": model.company_group
        };
        viewModels.push(viewModel);
      });
      return viewModels;
    };

    var getHsaPlanByCompanyGroup = function(companyGroupId) {
      return HsaRepository.ByCompanyGroup.query({groupId: companyGroupId}).$promise
      .then(function(response) {
        var mapped = mapCompanyGroupHsaPlansToViewModels(response);
        return mapped;
      });
    };

    return {
      GetCompanyHsaPlanByCompany: getCompanyHsaPlanByCompany,
      CreateHsaPlanForCompany: createHsaPlanForCompany,
      DeleteCompanyHsaPlan: deleteCompanyHsaPlan,
      GetHsaPlanEnrollmentByUser: getHsaPlanEnrollmentByUser,
      EnrollHsaPlanForEmployee: enrollHsaPlanForEmployee,
      RemoveHsaPlanForEmployee: removeHsaPlanForEmployee,
      GetHsaPlanByCompanyGroup: getHsaPlanByCompanyGroup
    };
  }
]);
