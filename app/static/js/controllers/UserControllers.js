// User controllers
var userControllers = angular.module('benefitmyApp.users.controllers', []);

var modalInstanceController = userControllers.controller(
  'modalInstanceController',
  ['$scope',
   '$state',
   '$modalInstance',
   'title',
   'message',
    function modalInstanceController(
      $scope,
      $state,
      $modalInstance,
      title,
      message){

        $scope.title = title;
        $scope.message = message;

        $scope.ok = function () {
          $modalInstance.close();
        };

    }]);

var modalMessageControllerBase = userControllers.controller(
  'modalMessageControllerBase',
  ['$scope',
   '$state',
   '$modal',
    function modalMessageControllerBase(
      $scope,
      $state,
      $modal){

        $scope.showMessageWithOkayOnly = function(title, message){
          $scope.title = title;
          $scope.message = message;
          var modalInstance = $modal.open({
            templateUrl: '/static/partials/modal_message_ok_only.html',
            controller: 'modalInstanceController',
            size: 'sm',
            backdrop: 'static',
            resolve: {
              title: function(){
                return $scope.title;
              },
              message: function(){
                return $scope.message;
              }
            }
          });
        };
    }]);

var findViewController = userControllers.controller('findViewController',
    ['$scope', '$location', 'currentUser', 'clientListRepository',
    function findViewController($scope, $location, currentUser, clientListRepository){
      var currentUser;
      var userRolesContains = function(userType, userRoles)
      {
        var role = _.findWhere(userRoles, {company_user_type:userType});
        return role != null;
      };

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
      };

      currentUser.get().$promise.then(function(response){
          determineDashboardLocation(response.roles);
      });
    }
]);

var userController = userControllers.controller('userController',
  ['$scope',
   '$http',
   '$location',
   '$modal',
   '$state',
   'UserService',
   'userLogOut',
   'CompanyEmployeeSummaryService',
   'CompanyFeatureService',
   'BrowserDetectionService',
   'EmployeeBenefitsAvailabilityService',
  function userController($scope,
                          $http,
                          $location,
                          $modal,
                          $state,
                          UserService,
                          userLogOut,
                          CompanyEmployeeSummaryService,
                          CompanyFeatureService,
                          BrowserDetectionService,
                          EmployeeBenefitsAvailabilityService) {
    $scope.roleArray = [];
    $scope.currentRoleList = [];
    var roleTypeDictionary = {
        admin:'Employer',
        broker:'Broker',
        employee: 'Employee'
    };

    UserService.getCurUserInfo().then(function(userInfo){
      $scope.curUser = userInfo.user;
      $scope.currentRoleList = userInfo.roles;
      $scope.company_id = userInfo.currentRole.company.id;

      CompanyFeatureService.getDisabledCompanyFeatureByCompany($scope.company_id).then(function(features) {
        $scope.disabledFeatures = features;
      });
      EmployeeBenefitsAvailabilityService.getEmployeeAvailableBenefits(
          $scope.company_id,
          userInfo.user.id)
      .then(function(availableBenefits){
        $scope.availableBenefits = availableBenefits;
      });
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
      return UserService.getCurrentRole()
    };

    $scope.getCurRoleString = function(){
      return roleTypeDictionary[$scope.getCurRoleFromPath()];
    }

    $scope.isCurRoleAdmin = function(){
      return $scope.getCurRoleFromPath() === 'admin';
    };

    $scope.isCurRoleBroker = function(){
      return $scope.getCurRoleFromPath() === 'broker';
    };

    $scope.isCurRoleEmployee = function(){
      return $scope.getCurRoleFromPath() === 'employee';
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

    // Not sure if it's a good idea to get the company id when first load the page
    // Could it be the user act so quickly and the company id has not been returned yet?
    $scope.downloadEmployeeSummaryReport = function(){
      var link = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryExcelUrl($scope.company_id);
      location.href = link;
    };

    $scope.downloadEmployeeDirectDepositReport = function(){
      var link = CompanyEmployeeSummaryService.getCompanyEmployeeDirectDepositExcelUrl($scope.company_id);
      location.href = link;
    };

    $scope.downloadCompanyEmployeeLifeBeneficiaryReport = function(){
      var link = CompanyEmployeeSummaryService.getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl($scope.company_id);
      location.href = link;
    };

    $scope.downloadCompanyEmployeeBenefitSummaryPDF = function(){
      var link = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryPdfUrl($scope.company_id);
      location.href = link;
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

    $scope.goToFunctionalViewByCompanyId = function(viewLink, parameter){
      if (!parameter){
        parameter = '';
      }
      $location.path(viewLink + $scope.company_id).search(parameter);
    };

    $scope.addOfferTemplate = function(){
      $state.go('document_templates_edit', {company_id:$scope.company_id});
    };

    $scope.gotoSettings = function(){
      $state.go('settings', {user_id: $scope.curUser.id});
    };

    $scope.startModifyBenefit = function() {
        // Show a modal dialog to take in the reason
        var curRole = $scope.getCurRoleFromPath();
        if(curRole)
        {
            var id = getIdByRole(curRole);
            var modalInstance = $modal.open({
                templateUrl: '/static/partials/benefit_selection/modal_pre_benefit_selection.html',
                controller: 'preBenefitSelectionModalController',
                size: 'md',
                backdrop: 'static'
              });

            modalInstance.result.then(function(reason){
                // Now proceed to the modify benefit view
                $state.go('employee_benefit_signup',
                    { employee_id: id,
                      updateReason: reason });
            });
        }
    };
}]);

var preBenefitSelectionModalController = userControllers.controller('preBenefitSelectionModalController',
  ['$scope',
   '$modalInstance',
   'BenefitUpdateReasonService',
    function($scope,
             $modalInstance,
             BenefitUpdateReasonService) {

        $scope.reason = {};

        BenefitUpdateReasonService.getAllReasons().then(function(categories) {
            $scope.categories = categories;
        });

        $scope.cancel = function() {
            $modalInstance.dismiss('cancelByUser');
        };

        $scope.proceed = function() {
            $modalInstance.close($scope.reason);
        };
    }
  ]);

var settingsController = userControllers.controller('settingsController', ['$scope',
   '$location',
   '$state',
   '$stateParams',
   'currentUser',
   'userSettingService',
   'PersonService',
   function settingsController ($scope, $location, $state, $stateParams, currentUser, userSettingService, PersonService){
      $('body').removeClass('onboarding-page');

      $scope.onboard = $stateParams.onboard;
      $scope.employeeId = $stateParams.user_id;

      $scope.editPersonal = function(event){
        $scope.isUpdatePersonalInfo = true;
        $scope.isUpdatePassword = false;
      };

      $scope.editPersonal();

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

var company1095CModalController = userControllers.controller('company1095CModalController',
    ['$scope',
     '$modal',
     '$modalInstance',
     'Company1095CService',
     'CompanyId',
     'Existing1095CData',
     function company1095CModalController ($scope,
                                           $modal,
                                           $modalInstance,
                                           Company1095CService,
                                           CompanyId,
                                           Existing1095CData){
      $scope.sorted1095CData = Existing1095CData;
      $scope.companyId = CompanyId
      if(!$scope.sorted1095CData){
        Company1095CService.get1095CByCompany($scope.companyId)
        .then(function(comp1095C){
          $scope.sorted1095CData = comp1095C;
        });
      }

      $scope.save = function(){
        Company1095CService.save1095CWithCompany($scope.companyId, $scope.sorted1095CData)
        .then(function(savedResponse){
          $modalInstance.close(savedResponse);
        }, function(errorResponse){
          alert('Saving 1095C form data failed. Error:' + errorResponse);
        });
      };

      $scope.cancel = function(){
        $modalInstance.dismiss("cancelled");
      };
    }
]);

var employee1095CModalController = userControllers.controller('employee1095CModalController', [
  '$scope',
  '$modal',
  '$modalInstance',
  'PersonService',
  'CompanyId',
  'Company1095CData',
  'EmployeeId',
  'Employee1095CService',
  function($scope,
           $modal,
           $modalInstance,
           PersonService,
           CompanyId,
           Company1095CData,
           EmployeeId,
           Employee1095CService) {

    var personId = null;

    PersonService.getSelfPersonInfo(EmployeeId).then(function(person) {
      personId = person.id;
      Employee1095CService.Get1095CByPersonCompany(CompanyId, person.id)
      .then(function(response) {
        $scope.employee1095CData = response;
      });
    });

    $scope.sorted1095CData = Company1095CData;
    $scope.employeeId = EmployeeId;

    $scope.save = function() {
      Employee1095CService.Save1095CForEmployee(personId, CompanyId, $scope.employee1095CData)
      .then(function(savedResponse) {
        $modalInstance.close(savedResponse);
      }, function(errorResponse) {
        alert('Saving employee safe harbor code failed. Error: ' + errorResponse);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss("cancelled");
    };
  }
]);

var Company1094CModalController = userControllers.controller('Company1094CModalController', [
  '$scope',
  '$modal',
  '$modalInstance',
  'Company1094CService',
  'CompanyId',
  'EligibilityCertification',
  'Company1094CData',
  function($scope,
           $modal,
           $modalInstance,
           Company1094CService,
           CompanyId,
           EligibilityCertification,
           Company1094CData) {

    var personId = null;

    $scope.sorted1094CData = Company1094CData;
    $scope.certifications = EligibilityCertification;

    $scope.booleans = {
      "TRUE": true,
      "FALSE": false
    };

    $scope.save = function() {
      Company1094CService.Save1094CWithCompany(CompanyId, $scope.sorted1094CData)
      .then(function(savedResponse) {
        $modalInstance.close(savedResponse);
      }, function(errorResponse) {
        alert('Saving employee safe harbor code failed. Error: ' + errorResponse);
      });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss("cancelled");
    };
  }
]);
