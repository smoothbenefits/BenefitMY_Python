var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyServiceProviderService',
    ['$q', 'CompanyServiceProviderRepository',
    function ($q, CompanyServiceProviderRepository){

        var PROVIDER_TYPES = {
            payroll: 'payroll',
            benefits: 'benefits'
        };

        var mapProviderViewModelToDomainModel = function(viewModel, companyId) {
          var domainModel = {
            company: companyId,
            show_to_employee: viewModel.showToEmployee,
            provider_type: viewModel.providerType,
            phone: viewModel.phone,
            email: viewModel.email,
            link: viewModel.link
          };

          if (viewModel.id) {
            domainModel.id = viewModel.id;
          }

          return domainModel;
        };

        var mapProviderDomainModelToViewModel = function(domainModel) {
          var viewModel = angular.copy(domainModel);
          viewModel.showToEmployee = domainModel.show_to_employee;
          viewModel.providerType = domainModel.providerType;
        };

        var getProvidersByCompany = function(companyId) {
          return CompanyServiceProviderRepository.ByCompany
            .query({companyId: companyId}).$promise
            .then(function(response) {
               var providers = [];
               _.each(response, function(provider) {
                 var viewModel = mapProviderDomainModelToViewModel(provider);
                 providers.push(viewModel);
               });
               return providers;
             });
        };

        var addCompanyServiceProvider = function(companyId, provider) {
          var domainModel = mapProviderViewModelToDomainModel(provider, companyId);
          return CompanyServiceProviderRepository.ById.save({}, domainModel).$promise;
        };

        var updateCompanyServiceProvider = function(companyId, provider) {
          var domainModel = mapProviderViewModelToDomainModel(provider, companyId);
          return CompanyServiceProviderRepository.ById
                 .update({entryId: domainModel.id}, domainModel).$promise;
        };

        var deleteProvider = function(entryId) {
          return CompanyServiceProviderRepository.ById.delete({entryId: entryId}).$promise;
        };

        return {
            ProviderTypes: PROVIDER_TYPES,
            GetProvidersByCompany: getProvidersByCompany,
            AddCompanyServiceProvider: addCompanyServiceProvider,
            UpdateCompanyServiceProvider: updateCompanyServiceProvider,
            DeleteProvider: deleteProvider
        };
    }
]);
