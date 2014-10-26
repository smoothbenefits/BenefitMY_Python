var BenefitMyHome = angular.module('BenefitMyHome',[
    'benefitmyService',
    'benefitMyHomeControllers']);


var benefitMyHomeControllers = angular.module('benefitMyHomeControllers',[]);

var homeUserController = benefitMyHomeControllers.controller('homeUserController', ['$scope', '$location', 'currentUser', 'userLogOut',
    function($scope, $location, currentUser, userLogOut){
        currentUser.get()
          .$promise.then(function(response)
               {
                  $scope.curUser = response.user;
                  $scope.userLoggedIn = true;
               },
               function(response)
               {
                  $scope.curUser=null;
                  $scope.userLoggedIn = false;
               }
          );
        $scope.logout = function ()
        {
            $scope.userLoggedIn = false;
            userLogOut.delete()
            .$promise.then(
              function(response){
                window.location = '/';
              },
              function(response)
              {
                window.location = '/';
              });
        }
    }                                                             
]);