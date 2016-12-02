BenefitMyApp.directive('bmOpenEnrollmentDefinition', function() {
  var openEnrollmentEditModalController = [
    '$scope',
    '$modalInstance',
    'OpenEnrollmentDefinitionService',
    'DateTimeService',
    'companyId',
    'openEnrollmentDefinition',
    function openEnrollmentEditModalController(
      $scope,
      $modalInstance,
      OpenEnrollmentDefinitionService,
      DateTimeService,
      companyId,
      openEnrollmentDefinition){
        $scope.init = function(){
          $scope.companyId = companyId;
          $scope.monthsInYear = DateTimeService.GetMonthsInYear();
          $scope.daysInMonth = DateTimeService.GetDaysInMonth();
          $scope.definition = openEnrollmentDefinition;
          $scope.definition.company = $scope.companyId;
        };
        $scope.cancel = function(){
          $modalInstance.dismiss();
        };
        $scope.save = function(){
          OpenEnrollmentDefinitionService.Save($scope.definition)
          .then(function(saved){
            $modalInstance.close(saved);
          });
        };
      }
  ];

  var controller = [
    '$scope',
    '$state',
    '$modal',
    '$controller',
    'OpenEnrollmentDefinitionService',
    function openEnrollmentViewController(
      $scope,
      $state,
      $modal,
      $controller,
      OpenEnrollmentDefinitionService) {

      $scope.init = function(){
        // Inherit base modal controller for dialog window
        $controller('modalMessageControllerBase', {$scope: $scope});
        
        $scope.$watch('companyId', function(compId) {
          if(!compId){
            return;
          }
          OpenEnrollmentDefinitionService.Get($scope.companyId)
          .then(function(openEnrollmentDef){
            $scope.openEnrollment = openEnrollmentDef;
          });
        });
      };

      $scope.editOpenEnrollment = function(){
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/common/model_open_enrollment_definition_edit.html',
            controller: openEnrollmentEditModalController,
            size: 'md',
            backdrop: 'static',
            resolve: {
              companyId: function(){
                return $scope.companyId;
              },
              openEnrollmentDefinition: function(){
                return angular.copy($scope.openEnrollment || {});
              },
            }
          });

          modalInstance.result.then(function(openEnrollmentDef){
            var successMessage = "The Open Enrollment Period has been saved successfully.";

            $scope.showMessageWithOkayOnly('Success', successMessage);
            
            $scope.openEnrollment = openEnrollmentDef;
          });
      };

      $scope.deleteOpenEnrollment = function(){
        OpenEnrollmentDefinitionService.Delete($scope.companyId)
        .then(function(deleted){
          var successMessage = "The Open Enrollment Period is removed";
          $scope.showMessageWithOkayOnly('Success', successMessage);
          $scope.openEnrollment = deleted;
        })
      }
    }
  ];
  return {
    restrict: 'E',
    scope: {
      companyId: '=',
    },
    templateUrl: '/static/partials/common/directive_open_enrollment_definition.html',
    controller: controller
  };
});
