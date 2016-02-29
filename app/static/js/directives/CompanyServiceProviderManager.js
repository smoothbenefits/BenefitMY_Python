BenefitMyApp.controller('CompanyServcieProviderController', [
  '$scope', '$state', '$modal', '$controller', 'CompanyServiceProviderService',
  function($scope, $state, $modal, $controller, CompanyServiceProviderService) {
    // Inherit base modal controller for dialog window
    $controller('modalMessageControllerBase', {$scope: $scope});
    var companyId = $scope.company;

    CompanyServiceProviderService.GetProvidersByCompany(companyId)
    .then(function(providers) {
      $scope.providers = providers;
      $scope.groupedProviders = _.groupBy(providers, function(provider) {return provider.providerType;});
    });

    var deleteProvider = function(provider) {
      CompanyServiceProviderService.DeleteProvider(provider.id)
      .then(function(success) {
        $scope.showMessageWithOkayOnly('Success', provider.name + ' has been deleted successfully');
        $state.reload();
      }, function(error) {
        $scope.showMessageWithOkayOnly('Warn', 'There is an error when trying to delete ' + provider.name + '. Please again later.');
      });
    };

    $scope.addNewProvider = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/company_service_provider/modal_company_service_provider_edit.html',
        controller: 'CompanyServiceProviderAddModalController',
        size: 'lg',
        resolve: {
          companyId: function() {
            return companyId;
          }
        }
      });

      modalInstance.result.then(function(group) {
        $state.reload();
      });
    };

    $scope.editProvider = function(provider) {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/company_service_provider/modal_company_service_provider_edit.html',
        controller: 'CompanyServiceProviderEditModalController',
        size: 'lg',
        resolve: {
          companyId: function() {
            return companyId;
          },
          provider: function() {
            return $scope.provider;
          }
        }
      });

      modalInstance.result.then(function(group) {
        $state.reload();
      });
    };
  }
])
.controller('CompanyServiceProviderEditModalController', [
  '$scope', '$modalInstance', 'CompanyServiceProviderService', 'companyId', 'provider',
  function($scope, $modalInstance, CompanyServiceProviderService, companyId, provider) {
    $scope.provider = angular.copy(provider);

    $scope.save = function() {
      CompanyServiceProviderService.UpdateCompanyServiceProvider(companyId, $scope.provider)
      .then(function(response) {
        $modalInstance.close(response);
      }, function(error) {
        $modalInstance.close(error);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
])
.controller('CompanyServiceProviderAddModalController', [
  '$scope', '$modalInstance', 'CompanyServiceProviderService', 'companyId',
  function($scope, $modalInstance, CompanyServiceProviderService, companyId) {
    $scope.provider = { providerType: 'payroll' };
    $scope.providerTypes = CompanyServiceProviderService.ProviderTypes;

    $scope.save = function() {
      CompanyServiceProviderService.AddCompanyServiceProvider(companyId, $scope.provider)
      .then(function(response) {
        $modalInstance.close(response);
      }, function(error) {
        $modalInstance.close(error);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss();
    };
  }
])
.directive('bmCompanyServiceProviderManager', function() {

  return {
    restrict: 'E',
    scope: {
      company: '=',
      editable: '='
    },
    templateUrl: '/static/partials/company_service_provider/directive_company_service_provider_manager.html',
    controller: 'CompanyServcieProviderController'
  };
});
