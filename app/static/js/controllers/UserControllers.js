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
           $location.replace().path('/'+firstRole);
        }
        else
        {
          window.location.replace('/error?role_match=false');
        }
      }

      currentUser.get()
      .$promise.then(function(response){
          determineDashboardLocation(response.roles);
       });
    }
]);

var userController = userControllers.controller('userController', 
  ['$scope', 
   '$http', 
   '$location', 
   'currentUser',
   'users', 
   'userLogOut', 
   'clientListRepository',
   'benefitSectionGlobalConfig',
  function userController($scope, 
                          $http, 
                          $location, 
                          currentUser, 
                          users, 
                          userLogOut, 
                          clientListRepository,
                          benefitSectionGlobalConfig) {
    $scope.roleArray = [];
    $scope.currentRoleList = [];
    var userPromise = currentUser.get()
      .$promise.then(function(response){
          $scope.curUser = response.user;
          $scope.currentRoleList = response.roles;
       });
    
    $scope.isRoleActive = function(checkRole){
      var roleFind = _.findWhere($scope.currentRoleList, {'company_user_type':checkRole});
      return !_.isUndefined(roleFind);
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
      return $scope.curUser.id;
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

    $scope.goToFunctionalViewByCompanyId = function(viewLink){
      currentUser.get().$promise.then(function(user){
        clientListRepository.get({userId: user.user.id}).$promise.then(function(response){
          var company = _.find(response.company_roles, {company_user_type: 'admin'});
          $location.path(viewLink + company.company.id);
        });
      });
    };

    $scope.gotoSettings = function(){
      $location.path('/settings');
    };

    // turn on/off benefit section globally here
    // need to move to a company profile which controls sections by company
    $scope.supplementalLifeInsuranceEnabled = 
      (_.find(benefitSectionGlobalConfig, {section_name: 'supplemental_life_insurance'})).enabled;
}]);

var settingsController = userControllers.controller('settingsController', ['$scope',
   '$location',
   '$stateParams',
   'currentUser',
   'userSettingService',
   'personInfoService',
   function settingsController ($scope, $location, $stateParams, currentUser, userSettingService, personInfoService){
      $('body').removeClass('onboarding-page');
      $scope.profile = {};
      $scope.forced = $stateParams.forced;
      currentUser.get()
        .$promise.then(function(response){
          $scope.curUser = response.user;
          $scope.showEmergencyContact = _.findWhere(response.roles, {company_user_type:'employee'});
          personInfoService.getPersonInfo($scope.curUser.id, function(basicInfo){
            if(basicInfo){
              $scope.person = basicInfo;
              $scope.person.hasInfo = true;
            }
          })
        });
      $scope.editPersonal = function(event){
        $scope.isUpdatePersonalInfo = true;
        $scope.isUpdatePassword = false;
      };

      $scope.editPersonal();

      $scope.updateBasicInfo = function(){
        personInfoService.savePersonInfo($scope.curUser.id, $scope.person, function(response){
          alert('Changes saved successfully');
          $location.path('/');
        }, function(errorResponse){
          alert('Failed to add the basic info. The error is: ' + 
                JSON.stringify(errorResponse.data) + 
                '\n and the http status is: ' + errorResponse.status);
        });
      };


      $scope.changePassword = function(event){
        $scope.isUpdatePersonalInfo = false;
        $scope.isUpdatePassword = true;
      };

      $scope.saveNewPassword = function(){
        //first we need to make sure the two passwords match
        if($scope.profile.new_password !== $scope.profile.confirm_new_password){
          alert('The passwords do not match. Please enter your new password again!')
          return false;
        }
        $scope.profile.username = $scope.curUser.email;
        userSettingService.save($scope.profile)
          .$promise.then(function(response){
            alert('Changes saved successfully');
            $location.path('/');
          }, function(error){
            if(error.status == 401){
              alert('The current password is not correct for the current user. Please try again.')
            }
            else{
              alert('Error: '+ error.data.error + '. Please try again.');
            }
          });
      }
  }]);