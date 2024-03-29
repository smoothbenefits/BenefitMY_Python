BenefitMyApp.directive('bmCredentialUpdate', function() {

  var controller = [
    '$scope',
    '$location',
    '$controller',
    'UserCredentialService',
    function CredentialUpdateDirectiveController(
      $scope,
      $location,
      $controller,
      UserCredentialService) {

        // Inherite scope from base
        $controller('modalMessageControllerBase', {$scope: $scope});

        var targetUserId = $scope.target;

        $scope.validPassword = function() {
          if (!$scope.newPassword) {
            return false;
          }

          if (!$scope.passwordRepeat) {
            return false;
          }

          if ($scope.newPassword !== $scope.passwordRepeat) {
            return false;
          }

          if ($scope.newPassword.length < 8) {
            return false;
          }

          return true;
        };

        $scope.save = function () {
          if (!$scope.validPassword()) {
            var errorMessage = 'Please make sure you provide a valid password. \n';

            if ($scope.newPassword !== $scope.passwordRepeat) {
              errorMessage += 'Re-entered password does not match the original value. \n';
            }

            if ($scope.newPassword.length < 8) {
              errorMessage += 'Password should be at least 8-charater long. \n';
            }
            $scope.showMessageWithOkayOnly('Error', errorMessage);
          } else {
            UserCredentialService.UpdateUserCredential(targetUserId, $scope.newPassword)
            .then(function() {
              $scope.showMessageWithOkayOnly('Success', 'Changes are saved successfully.');
              $scope.resetPassword();
              $location.reload();
            }, function(error) {
              $scope.showMessageWithOkayOnly('Error', 'Failed to update. ' + error);
              $scope.resetPassword();
            });
          }
        };

      $scope.resetPassword = function() {
        $scope.newPassword = '';
        $scope.passwordRepeat = '';
      };
    }
  ];

  return {
    restrict: 'E',
    scope: {
        target: '='
    },
    templateUrl: '/static/partials/common/directive_credential_update.html',
    controller: controller
  };
});
