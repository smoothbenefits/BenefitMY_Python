BenefitMyApp.directive('bmDirectDepositManager', function() {

  var directDepositModalController = [
   '$scope',
   '$state',
   '$modalInstance',
   '$q',
   'DirectDepositService',
   'directDepositAccount',
   'userId',
    function($scope,
             $state,
             $modalInstance,
             $q,
             DirectDepositService,
             directDepositAccount,
             userId){

      $scope.errorMessage = null;
      $scope.account = directDepositAccount;
      $scope.bankAccountTypes = ['Checking', 'Saving'];

      // wrap up add/edit service call
      var directDepositPromise = function(account){
        var deferred = $q.defer();
        var directDeposit = DirectDepositService.mapViewDirectDepositToDto(account);

        // check if the account has an id. If yes, update the account
        if (directDeposit.id){
          DirectDepositService.updateDirectDepositById(directDeposit).then(function(response){
            deferred.resolve(response);
          }, function(error){
            deferred.reject(error);
          });
        }
        else{
          DirectDepositService.createDirectDepositByUserId(userId, directDeposit).then(function(response){
            deferred.resolve(response);
          }, function(error){
            deferred.reject(error);
          });
        }
        return deferred.promise;
      };

      $scope.amountDisabled = function(account){
        return account.percentage && account.percentage != 0;
      };

      $scope.percentageDisabled = function(account){
        return account.amount && account.amount != 0;
      };

      $scope.cancel = function() {
        $modalInstance.dismiss('cancelByUser');
      };

      $scope.save = function(account) {
        directDepositPromise(account).then(function(response){
          $modalInstance.close(response);
        }, function(error){
          $scope.errorMessage = "Error occurred when tried to save direct deposit. Please verify " +
            "all the information enterred are valid. Message: " + error;
        });
      };
    }
  ];

  var directiveController = [
    '$scope',
    '$attrs',
    '$state',
    '$stateParams',
    '$controller',
    '$modal',
    'UserService',
    'DirectDepositService',
    function DirectDepositManagerDirectiveController(
        $scope,
        $attrs,
        $state,
        $stateParams,
        $controller,
        $modal,
        UserService,
        DirectDepositService) {

        // Inherit base modal controller for dialog window
        $controller('modalMessageControllerBase', {$scope: $scope});

        $scope.$watch('userId', function(userId) {
            if (userId) {
              DirectDepositService.getDirectDepositByUserId(userId).then(function(response){
                $scope.directDepositAccounts = DirectDepositService.mapDtoToViewDirectDepositInBulk(response);
              });
            }
        });

        $scope.addDirectDepositAccount = function(){
          DirectDepositService.getEmptyDirectDepositAccount().then(function(account){
            $scope.editDirectDepositAccount(account);
          }, function(error){
            alert('Found error when tried to add a new account. Please try again later.');
          });
        };

        $scope.editDirectDepositAccount = function(account){
          var accountCopy = angular.copy(account);

          var modalInstance = $modal.open({
            templateUrl: '/static/partials/payroll/modal_direct_deposit.html',
            controller: directDepositModalController,
            size: 'lg',
            backdrop: 'static',
            resolve: {
              directDepositAccount: function () {
                return accountCopy;
              },
              userId: function() {
                return $scope.userId;
              }
            }
          });

          modalInstance.result.then(function(account){
            var successMessage = "Your direct deposit account has been saved. " +
                  "You can return to dashboard through left navigation panel. " +
                  "Or add another account using the button below.";

            $scope.showMessageWithOkayOnly('Success', successMessage);

            var updatedAccount = DirectDepositService.mapDtoToViewDirectDeposit(account);
            var accountInView = _.findWhere($scope.directDepositAccounts, {id: updatedAccount.id});
            if (accountInView){
              var index = $scope.directDepositAccounts.indexOf(accountInView);
              $scope.directDepositAccounts[index] = updatedAccount;
            }
            else{
              $scope.directDepositAccounts.push(updatedAccount);
            }
          });
        };

        $scope.deleteDirectDepositAccont = function(account){

          var confirmed = confirm('About to delete a direct deposit account. Are you sure?');
          if (confirmed === true){

            var directDeposit = DirectDepositService.mapViewDirectDepositToDto(account);
            DirectDepositService.deleteDirectDepositById(directDeposit).then(function(response){
              var successMessage = "Your direct deposit account has been deleted. " +
                  "You can return to dashboard through left navigation panel. " +
                  "Or add another account using the button below.";

              $scope.showMessageWithOkayOnly('Success', successMessage);

              // remove deteled account from $scope object
              $scope.directDepositAccounts = _.reject($scope.directDepositAccounts, {id: response.id});
            }, function(error){
              var errorMessage = "Error occurred when tried to delete your direct deposit account. " +
                  "Please try again later. Error message: " + error;
              $scope.showMessageWithOkayOnly('Error', errorMessage);
            });
          }
        };

        $scope.getFinishButtonDisplayText = function() {
            if ($scope.directDepositAccounts 
                && $scope.directDepositAccounts.length > 0) {
                return 'Finish & Proceed';
            } else {
                return 'Skip & Proceed';
            }
        };

        $scope.finishAndProceed = function() {
            if ('onFinish' in $attrs) {
                $scope.onFinish();
            }
        };

        $scope.showFinishButton = function() {
            return 'onFinish' in $attrs;
        };
    }
  ];

  return {
    restrict: 'E',
    scope: {
      userId: '=',
      headerText: '=?',
      onFinish: '&'
    },
    templateUrl: '/static/partials/payroll/directive_direct_deposit_manager.html',
    controller: directiveController
  };
});
