BenefitMyApp.directive('bmEdit1094c', function() {
    
    var controller = ['$scope',
                      '$modal',
                      'Company1094CService',
                      function($scope,
                               $modal,
                               Company1094CService) {

        var companyId = $scope.company;

        Company1094CService.Get1094CEligibilityCertification().then(function(data) {
          $scope.eligibilityCertification = data;
        });

        Company1094CService.Get1094CByCompany(companyId).then(function(data) {
          $scope.sorted1094CData = data;
        });

        $scope.getCompany1094CUrl = function() {
          return Company1094CService.GetCompany1094CUrl(companyId);
        };

        $scope.edit1094CInfo = function() {
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/aca/modal_company_1094_c.html',
            controller: 'Company1094CModalController',
            size: 'lg',
            backdrop: 'static',
            resolve: {
              CompanyId: function() { return companyId; },
              EligibilityCertification: function() { return $scope.eligibilityCertification; },
              Company1094CData: function() {
                return angular.copy($scope.sorted1094CData);
              }
            }
          });

          modalInstance.result.then(function(saved1094CData) {
            $scope.sorted1094CData = saved1094CData;
            if($scope.onSuccess){
                $scope.onSuccess('Success', 'Company 1094C data has been saved successfully.');
            }
          });
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
      company: '=',
      onSuccess: '=?'
    },
    templateUrl: '/static/partials/common/aca_report_summary.html',
    controller: controller
  };
});