var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('IntegrationProviderService',
    ['$q',
    'IntegrationProvideRepository',
    function (
        $q, 
        IntegrationProvideRepository){

        var IntegrationProviderServiceTypes = {
            Payroll: 'Payroll'
        };

        var IntegrationProviderNames = {
            AdvantagePayroll: 'Advantage Payroll',
            ContentPayroll: 'Connect Payroll'
        };

        var integrationProvidersByCompanyIdCache = {};

        var mapIntegrationProviderDomainToViewModel = function(domainModel) {
            var viewModel = {};

            viewModel.providerName = domainModel.integration_provider.name;
            viewModel.serviceType = domainModel.integration_provider.service_type;
            viewModel.companyExternalId = domainModel.company_external_id;

            return viewModel;
        };

        var mapCompanyIntegrationProvidersDomainToViewModel = function(domainModel) {
            var viewModel = {};

            for (var key in domainModel) {
                viewModel[key] = mapIntegrationProviderDomainToViewModel(domainModel[key]);
            }

            // Attach utility functions
            viewModel.isActiveProvider = function(serviceType, providerName) {
                return this[serviceType] && this[serviceType].providerName == providerName;
            };

            return viewModel;
        };

        var getIntegrationProvidersByCompany = function(companyId) {
            var deferred = $q.defer();

            if (integrationProvidersByCompanyIdCache[companyId]) {
                deferred.resolve(integrationProvidersByCompanyIdCache[companyId]);
            } else {
                IntegrationProvideRepository.ByCompany.get({companyId: companyId})
                .$promise.then(
                    function(integrationProviders) {
                        integrationProvidersByCompanyIdCache[companyId] = integrationProviders;
                        deferred.resolve(integrationProviders);
                    },
                    function(errors) {
                        deferred.reject(errors);
                    }
                );
            }

            return deferred.promise;
        };

        var companyHasIntegrationProviderByServiceType = function(companyId, serviceType) {
            return getIntegrationProvidersByCompany(companyId).then(function(providers) {
                return providers && providers[serviceType];
            });
        };

        return {
            
            IntegrationProviderServiceTypes: IntegrationProviderServiceTypes,
            IntegrationProviderNames: IntegrationProviderNames,

            getIntegrationProvidersByCompany: getIntegrationProvidersByCompany,
            companyHasIntegrationProviderByServiceType: companyHasIntegrationProviderByServiceType
        };
    }
]);
