BenefitMyApp.controller('CompanyServcieProviderController', [
  '$scope', '$state', '$modal', '$controller', 'CompanyServiceProviderService',
  function($scope, $state, $modal, $controller, CompanyServiceProviderService) {
    // Inherit base modal controller for dialog window
    $controller('modalMessageControllerBase', {$scope: $scope});

    $scope.$watch('company', function(companyId) {
      if(companyId){

        $scope.company = companyId;

        CompanyServiceProviderService.GetProvidersByCompany(companyId)
        .then(function(providers) {

          // If not admin, filter base on showToEmployee flag
          if ($scope.isAdmin) {
            $scope.providers = providers;
          } else {
            $scope.providers = _.filter(providers, function(provider) {
              return provider.showToEmployee;
            });
          }

          $scope.groupedProviders = _.groupBy($scope.providers, function(provider) {return provider.providerType;});
          $scope.presentedTypes = _.keys($scope.groupedProviders);
        });
      }
    });

    $scope.deleteProvider = function(provider) {
      CompanyServiceProviderService.DeleteProvider(provider.id)
      .then(function(success) {
        $scope.showMessageWithOkayOnly('Success', provider.name + ' has been deleted successfully');
        $state.reload();
      }, function(error) {
        $scope.showMessageWithOkayOnly('Error', 'There is an error when trying to delete ' + provider.name + '. Please again later.');
      });
    };

    $scope.addNewProvider = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/company_service_provider/modal_company_service_provider_edit.html',
        controller: 'CompanyServiceProviderAddModalController',
        size: 'lg',
        resolve: {
          companyId: function() {
            return $scope.company;
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
            return $scope.company;
          },
          provider: function() {
            return angular.copy(provider);
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
    $scope.provider = provider;

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
    $scope.provider = {};

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
      isAdmin: '='
    },
    templateUrl: '/static/partials/company_service_provider/directive_company_service_provider_manager.html',
    controller: 'CompanyServcieProviderController'
  };
});
