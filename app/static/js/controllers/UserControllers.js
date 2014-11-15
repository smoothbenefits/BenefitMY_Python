// User controllers
var userControllers = angular.module('benefitmyApp.users.controllers', []);


var findViewController = userControllers.controller('findViewController',
    ['$scope', '$location', 'currentUser', 'clientListRepository',
    function findViewController($scope, $location, currentUser, clientListRepository){
      var currentUser;
      var userRolesContains = function(userType, userRoles)
      {
        var role = _.findWhere(userRoles, {company_user_type:userType});
        return role != null;
      }
      var determineDashboardLocation = function(userRoles)
      {
        var urlParam = window.location.search;
        if(urlParam !== '')
        {
          var paramNameValueList = urlParam.split('=');
          var paramValue = paramNameValueList[1];
          if(userRolesContains(paramValue, userRoles))
          {
            $location.replace().path('/'+paramValue.toLowerCase());
          }
        }
        else if(userRoles.length > 0 && !paramValue)
        {
           var firstRole = userRoles[0].company_user_type;
           if(firstRole.toLowerCase() === 'employee'){
              $location.replace().path('/employee/onboard/index/' + currentUser.id);
           }
           else
           {
              $location.replace().path('/'+firstRole.toLowerCase());
           }
        }
        else
        {
          window.location.replace('/error?role_match=false');
        }
      }

      var userPromise = currentUser.get()
        .$promise.then(function(response)
             {
                currentUser = response.user;
                return currentUser;
             }
        );
      userPromise.then(function(user){
        clientListRepository.get({userId:user.id})
          .$promise.then(function(response){
            determineDashboardLocation(response.company_roles);
          });
      });
    }
]);

var userController = userControllers.controller('userController', ['$scope', '$http', 'currentUser','users', 'userLogOut', 'clientListRepository','$location',
  function userController($scope, $http, currentUser, users, userLogOut, clientListRepository, $location) {
    $scope.roleArray = [];
    var currentRoleList = [];
    var userPromise = currentUser.get()
        .$promise.then(function(response)
             {
                $scope.curUser = response.user;
                return $scope.curUser;
             }
        );
    $scope.isRoleActive = function(checkRole){
      if(currentRoleList.length <=0){
        userPromise.then(function(user){
          clientListRepository.get({userId:user.id})
            .$promise.then(function(response){
              currentRoleList = response.company_roles;
            });
        });
        return false;
      }
      else
      {
        var roleFind = _.findWhere(currentRoleList, {'company_user_type':checkRole.capitalize()});
        return !_.isUndefined(roleFind);
      }
    };
    $scope.logout = function ()
    {
        userLogOut.delete()
        .$promise.then(
          function(response){
            window.location = '/';
          },
          function(response)
          {
            window.location = '/';
          });
    };
    $scope.getCurRoleFromPath = function(){
      var curPath = $location.path();
      if(curPath[0] === '/'){
        curPath = curPath.substring(1);
      }
      var pathArray = curPath.split('/');
      if(pathArray.length > 0)
      {
        return pathArray[0];
      }
      else
      {
        return undefined;
      }
    };
    var getIdByRole = function(role){
      if(role === 'employee'){
        return $scope.curUser.id;
      }
      else{
        var curCompanyRole = _.findWhere(currentRoleList, {'company_user_type':role});
        return curCompanyRole.company.id;
      }
    };
    $scope.getActiveRoleClass = function(checkPath){
      var curPath = $location.path();

      if(curPath === checkPath)
      {
        return "active";
      }
      else
      {
        return "inactive";
      }
    };
    $scope.goToFunctionalView = function(viewLink, parameter){
      var curRole = $scope.getCurRoleFromPath();
      if(curRole)
      {
        var id = getIdByRole(curRole);
        if(parameter)
        {
          $location.path(viewLink+id).search(parameter);
        }
        else{
          $location.path(viewLink + id).search('');
        }
      }
    };
}]);
