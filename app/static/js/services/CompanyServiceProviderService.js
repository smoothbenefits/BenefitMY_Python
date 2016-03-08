var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyServiceProviderService',
    ['$q', 'CompanyServiceProviderRepository', 'utilityService',
    function ($q, CompanyServiceProviderRepository, utilityService){

        var mapProviderViewModelToDomainModel = function(viewModel, companyId) {
          var domainModel = {
            name: viewModel.name,
            company: companyId,
            show_to_employee: viewModel.showToEmployee,
            provider_type: viewModel.providerType,
            phone: viewModel.phone,
            email: viewModel.email,
            link: utilityService.normalizeLink(viewModel.link)
          };

          if (viewModel.id) {
            domainModel.id = viewModel.id;
          }

          return domainModel;
        };

        var mapProviderDomainModelToViewModel = function(domainModel) {
          var viewModel = angular.copy(domainModel);
          viewModel.showToEmployee = domainModel.show_to_employee;
          viewModel.providerType = domainModel.provider_type;

          // Make sure that the link is in right format, which is needed
          // for the anchor tag to operate.
          viewModel.link = utilityService.normalizeLink(viewModel.link);

          return viewModel;
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
            GetProvidersByCompany: getProvidersByCompany,
            AddCompanyServiceProvider: addCompanyServiceProvider,
            UpdateCompanyServiceProvider: updateCompanyServiceProvider,
            DeleteProvider: deleteProvider
        };
    }
]);
