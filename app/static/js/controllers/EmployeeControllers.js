var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
  ['$scope',
   '$location',
   '$state',
   '$stateParams',
   'UserService',
   'EmployeePreDashboardValidationService',
   'employeePayrollService',
   'EmploymentProfileService',
   'DirectDepositService',
   'DocumentService',
   'CompanyFeatureService',
   'CompanyPersonnelsService',
  function ($scope,
            $location,
            $state,
            $stateParams,
            UserService,
            EmployeePreDashboardValidationService,
            employeePayrollService,
            EmploymentProfileService,
            DirectDepositService,
            DocumentService,
            CompanyFeatureService,
            CompanyPersonnelsService){
    $('body').removeClass('onboarding-page');

    var curUserId;
    var userPromise = UserService.getCurUserInfo();

    // Get user information, and perform validation and redirect
    // upon landing
    userPromise.then(function(response){
      $scope.employee_id = response.user.id;
      $scope.company = response.currentRole.company;
      var employeeRole = _.findWhere(response.roles, {company_user_type:'employee'});
      if(employeeRole){
        EmployeePreDashboardValidationService.onboarding($scope.employee_id, function(){
          return response;
        }, function(redirectUrl){
          $location.path(redirectUrl);
        });
      }
      else{
        EmployeePreDashboardValidationService.basicInfo($scope.employee_id, function(){
          return response;
        }, function(){
          //we need to redirect to edit profile page
          $state.go('settings', {user_id: $scope.employee_id, onboard:1});
        });
      }
      CompanyPersonnelsService.getEmployeeDirectReportCount(
        $scope.company.id,
        $scope.employee_id
      ).then(function(count){
        $scope.directReportCount = count;
      });
      return response;
    });

    // Now start preparing all the data needed to pass to the
    // the module directives

    $scope.showBenefitSection = function() {
        return $scope.hasBenefits;
    };

    $scope.viewBenefits = function() {
        $state.go('employee_view_benefits');
    };

    $scope.showPayrollSection = function() {
        return $scope.showPayrollW4Section()
            || $scope.showPayrollDirectDepositSection();
    };

    $scope.showPayrollW4Section = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.W4);
    };

    $scope.showPayrollDirectDepositSection = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.DD);
    };

    $scope.viewPayrollW4 = function() {
        $state.go('employee_payroll.w4');
    };

    $scope.viewPayrollDirectDeposit = function() {
        $state.go('employee_payroll.direct_deposit');
    };

    $scope.viewUploads = function() {
        $state.go('employeeUploads');
    };

    $scope.showProfileI9 = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.I9);
    };

    $scope.viewProfileI9 = function() {
        $state.go('employee_profile.i9');
    };

    $scope.viewDocuments = function() {
        $state.go('employee_view_documents');
    };

    $scope.showTimeoff = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.Timeoff);
    };

    $scope.viewTimeoff = function() {
        $state.go('employeetimeoff');
    };

    $scope.showWorkTimesheets = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.WorkTimeSheet);
    };

    $scope.viewWorkTimesheets = function() {
        $state.go('employee_timesheet');
    };

    $scope.showTimePunchCards = function() {
        return $scope.allFeatureStatus 
            && $scope.allFeatureStatus.isFeatureEnabled(
                CompanyFeatureService.AppFeatureNames.RangedTimeCard);
    };

    $scope.showDirectReports = function(){
      return $scope.allFeatureStatus &&
        $scope.allFeatureStatus.isFeatureEnabled(
          CompanyFeatureService.AppFeatureNames.DirectReportsView
        ) &&
        $scope.directReportCount > 0;
    };

    $scope.viewDirectReports = function(){
      $state.go('employee_direct_reports_view');
    };

    $scope.viewTimePunchCards = function() {
        $state.go('employee_timepunchcard');
    };

    $scope.showTimeTrackingSection = function() {
        return $scope.showTimeoff()
            || $scope.showWorkTimesheets()
            || $scope.showTimePunchCards();
    };

    $scope.viewEmployeeSupportPage = function() {
      $state.go('employeeSupport');
    };
  }
]);

var employeeViewBenefits = employeeControllers.controller('employeeViewBenefits',
  ['$scope',
   '$state',
   '$stateParams',
   'UserService',
   function($scope,
            $state,
            $stateParams,
            UserService) {

     UserService.getCurUserInfo().then(function(userInfo){
       $scope.user = userInfo.user;
       $scope.company = userInfo.currentRole.company;
     });

     $scope.backToDashboard = function(){
       $state.go('/employee');
     };

   }
  ]);

var employeeViewDocuments = employeeControllers.controller('employeeViewDocuments',
  ['$scope',
   '$state',
   '$stateParams',
   'UserService',
   function($scope,
            $state,
            $stateParams,
            UserService) {

     UserService.getCurUserInfo().then(function(userInfo){
       $scope.user = userInfo.user;
       $scope.company = userInfo.currentRole.company;
     });

     $scope.documentViewerHeaderText = "Documents from my Employer";

     $scope.backToDashboard = function(){
       $state.go('/employee');
     };

   }
  ]);

var viewDocument = employeeControllers.controller('viewDocument',
  ['$scope', '$location', '$stateParams', 'DocumentService', 'currentUser', 'documentRepository',
  function viewDocument($scope, $location, $stateParams, DocumentService, currentUser, documentRepository){
    $scope.document = {};
    $scope.documentId = $stateParams.doc_id;
    var userPromise = currentUser.get().$promise
      .then(function(response){
        $scope.employee_id = response.user.id;
        return response.user.id;
      });

    var documentPromise = userPromise.then(function(userId){
      return DocumentService.getUserDocumentById(userId, $scope.documentId);
    });

    documentPromise.then(function(document){
      $scope.document = document;
      if(document.signature && document.signature.signature)
      {
        $scope.signatureId = $scope.document.signature.id;
      }
    });

    $scope.inTextMode = function() {
        return $scope.document
            && $scope.document.contentType == DocumentService.contentTypes.text;
    };

    $scope.inUploadMode = function() {
        return $scope.document
            && $scope.document.contentType == DocumentService.contentTypes.upload;
    };

    $scope.signDocument = function(signature){
        DocumentService.signUserDocument($scope.document.id, signature.id)
        .then(function(successResponse){
            alert("The document has been signed successfully.");
            $scope.goToDashboard();
        }, function(failureResponse){
            alert("There was a problem saving the signature.");
        });
    };

    $scope.goToDashboard = function()
    {
      $location.path('/employee');
    };
}]);

var employeePayroll = employeeControllers.controller('employeePayrollController',
  ['$scope',
   '$state',
   'tabLayoutGlobalConfig',
   function($scope,
            $state,
            tabLayoutGlobalConfig){
    $scope.section = _.findWhere(tabLayoutGlobalConfig, {section_name: 'employee_payroll'});

    $scope.goToState = function(state){
      $state.go(state);
    };

    $scope.backToDashboard = function(){
      $state.go('/employee');
    };
   }
  ]);

var employeeW4Controller = employeeControllers.controller('employeeW4Controller',
  ['$scope',
   '$state',
   '$window',
   'currentUser',
   'employeePayrollService',
   'utilityService',
   function($scope,
            $state,
            $window,
            currentUser,
            employeePayrollService,
            utilityService){
    var userPromise = currentUser.get().$promise.then(function(response){
      return response.user.id;
    });

    userPromise.then(function(userId){
      employeePayrollService.getEmployeeTaxSummaryByUserId(userId)
      .then(function(response){
        $scope.employee = employeePayrollService.mapW4DtoToView(response);
        $scope.fields = utilityService.mapObjectToKeyPairArray('w4', response);
      });
    });

    $scope.calculateTotal = function(){
      employeePayrollService.calculateTotalBasedOnViewW4($scope.employee);
    };

    $scope.userDefinedPointsSet = function(){
      $scope.employee.user_defined_set = true;
    };

    $scope.openW4File = function(){
      if($scope.employee.downloadW4){
        var link = angular.element('#w4doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.submit=function(){
      if(!$scope.employee.downloadW4){
        alert('Please verify you have downloaded and read the entire W-4 form');
        return;
      }
      if(typeof($scope.employee.dependent_count) === 'undefined'){
        alert('Please enter the number of dependents');
        return;
      }
      if(typeof($scope.employee.user_defined_points) === 'undefined'){
        alert('Please enter the final withholding number (line 5 on your W-4)');
        return;
      }
      if(typeof($scope.employee.extra_amount) === 'undefined'){
        $scope.employee.extra_amount = 0;
      }

      // Add marriage number to $scope object
      var dtoW4 = employeePayrollService.mapW4ViewToDto($scope.employee);
      userPromise.then(function(userId){
        employeePayrollService.saveEmployeeTaxByUserId(userId, dtoW4)
        .then(function(response){
          $state.go('employee_payroll.w4');
        });
      });
    };

    $scope.editW4 = function(){
      $state.go('employee_payroll.w4_edit');
    };
   }
  ]);

var employeeProfile = employeeControllers.controller('employeeProfileController',
  ['$scope',
   '$state',
   'tabLayoutGlobalConfig',
   function ($scope,
             $state,
             tabLayoutGlobalConfig){
    $scope.section = _.findWhere(tabLayoutGlobalConfig, { section_name: 'employee_profile'});

    $scope.goToState = function(state){
      $state.go(state);
    };

    $scope.backToDashboard = function(){
      $state.go('/employee');
    };
   }
  ]);

var employeeI9Controller = employeeControllers.controller('employeeI9Controller',
  ['$scope',
   '$state',
   '$window',
   'currentUser',
   'EmploymentProfileService',
   function($scope,
            $state,
            $window,
            currentUser,
            EmploymentProfileService){
    $scope.employee = {auth_type: ''};

    var userPromise = currentUser.get().$promise.then(function(response){
      return response.user.id;
    });

    userPromise.then(function(userId){
      // assign user id to current employee
      $scope.employee.userId = userId;

      EmploymentProfileService.getEmploymentAuthByUserId(userId).then(function(response){
        $scope.fields = response;
      });
    });

    $scope.openI9File = function(){
      if($scope.employee.downloadI9){
        var link = angular.element('#i9doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.signButtonText = "Submit";

    $scope.allowProceedWithSign = function() {
        return $scope.employee.downloadI9;
    };

    $scope.signDocument = function(signature){
        if($scope.employee.auth_type === 'Aaw' && !$scope.employee.expiration_na
         && !$scope.employee.auth_expiration) {
            alert('Please provide the expiration date for your work authorization document.');
            return;
        }

        EmploymentProfileService.saveEmploymentAuthByUserId($scope.employee, signature.id)
        .then(function(response){
          $state.go('employee_profile.i9');
        }, function(error){
          alert('Employment authorization has NOT been saved. Please try again later.');
        });
    };

    $scope.editI9 = function(){
      $state.go('employee_profile.i9_edit');
    };
   }
  ]);

var directDeposit = employeeControllers.controller('employeeDirectDepositController',
  ['$scope',
   'UserService',
   function($scope, UserService){
        var userPromise = UserService.getCurUserInfo().then(function(response){
          $scope.userId = response.user.id;
        });
  }]);

var stateTax = employeeControllers.controller('employeeStateTaxController',
  ['$scope',
   'UserService',
   function($scope, UserService){
        var userPromise = UserService.getCurUserInfo().then(function(response){
          $scope.userId = response.user.id;
        });
  }]);

var signIn = employeeControllers.controller('employeeSignin', ['$scope', '$stateParams', function($scope, $stateParams){
  $scope.employee = {};
  $scope.employee.id = $stateParams.employee_id;
  $scope.employee.username = '';
  $scope.employee.password = '';

  $scope.submit = function(employee) {
    // Need to add actions to validate sign in credentials
    return false;
  }
}]);

var signup = employeeControllers.controller('employeeSignup', ['$scope', '$stateParams', '$location',
  function($scope, $stateParams, $location){
    $scope.employee = {};
    $scope.employee.id = $stateParams.signup_number;

    $scope.submit = function(employee) {
      if($scope.employee.password !== $scope.employee.password_confirm)
      {
        alert('The passwords do not match. Please input your passwords again!');
      }
      else
      {
        // Need to communicate with API to register the new employee
        $location.path('/employee/signin/' + $scope.employee.id);
      }
    }
}]);

var onboardIndex = employeeControllers.controller('onboardIndex',
  ['$scope',
   '$state',
   '$stateParams',
   'tabLayoutGlobalConfig',
   'UserService',
   'CompanyFeatureService',
   function ($scope,
             $state,
             $stateParams,
             tabLayoutGlobalConfig,
             UserService,
             CompanyFeatureService){
    var companyFeaturesPromise = UserService.getCurrentRoleCompleteFeatureStatus().then(function(userInfo) {
        var company = userInfo.currentRole.company;
        return CompanyFeatureService.getAllApplicationFeatureStatusByCompany(company.id);
    });

    UserService.getCurrentRoleCompleteFeatureStatus().then(function(allFeatureStatus) {
        UserService.isCurrentUserNewEmployee().then(
            function(isNewEmployee) {
                var section = _.findWhere(tabLayoutGlobalConfig, { section_name: 'employee_onboard'});
                $scope.tabs = section.tabs;
                if (!isNewEmployee
                    || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.I9)) {
                    $scope.tabs = _.reject($scope.tabs, function(tab) {
                        return tab.name == 'employment';
                    });
                }
                if (!isNewEmployee
                    || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.W4)) {
                    $scope.tabs = _.reject($scope.tabs, function(tab) {
                        return tab.name == 'tax' || tab.name == 'state_tax';
                    });
                }
                if (!isNewEmployee
                    || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.DD)) {
                    $scope.tabs = _.reject($scope.tabs, function(tab) {
                        return tab.name == 'direct_deposit';
                    });
                }
            }
        );
    });
   }
  ]);

var onboardBasicInfo = employeeControllers.controller('onboardBasicInfo',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   'PersonService',
   'currentUser',
   'EmployeePreDashboardValidationService',
  function($scope,
           $state,
           $stateParams,
           $location,
           PersonService,
           currentUser,
           EmployeePreDashboardValidationService){

    $scope.employee = {};
    $scope.employeeId = $stateParams.employee_id;
    $scope.displayAll = false;

    EmployeePreDashboardValidationService.onboarding($scope.employeeId, function(){
      $location.path('/employee');
    },
    function(redirectUrl){
      if($location.path() !== redirectUrl){
        $location.path(redirectUrl);
      }
      else{
        $scope.displayAll = true;
      }
    });

    $('body').addClass('onboarding-page');

    PersonService.getSelfPersonInfo($scope.employeeId).then(function(self_data){
      $scope.employee = self_data;
    });

    $scope.addBasicInfo = function(){
      var birthDate = $scope.employee.birth_date;
      $scope.employee.birth_date = moment(birthDate).format('YYYY-MM-DD');
      PersonService.savePersonInfo($scope.employeeId, $scope.employee)
      .then(function(successResponse){
        $state.go('employee_onboard.employment', { employee_id: $scope.employeeId });
      }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
}]);

var onboardEmployment = employeeControllers.controller('onboardEmployment',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   '$window',
   'EmploymentProfileService',
   'EmployeePreDashboardValidationService',
  function($scope,
           $state,
           $stateParams,
           $location,
           $window,
           EmploymentProfileService,
           EmployeePreDashboardValidationService){
    $scope.employeeId = $stateParams.employee_id;

    $scope.employee = {
      auth_type: '',
      userId: $scope.employeeId
    };

    EmployeePreDashboardValidationService.onboarding($scope.employeeId, function(){
      $location.path('/employee');
    },
    function(redirectUrl){
      if($location.path() !== redirectUrl){
        $location.path(redirectUrl);
      }
      else{
        $scope.displayAll = true;
      }
    });

    $('body').addClass('onboarding-page');

    $scope.acknowledgedI9=function(){
      $scope.employee.downloadI9 = !$scope.employee.downloadI9;
    };

    $scope.openI9File = function(){
      if($scope.employee.downloadI9){
        var link = angular.element('#i9doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.signButtonText = "Sign and Next";

    $scope.allowProceedWithSign = function() {
        return $scope.employee.downloadI9;
    };

    $scope.signDocument = function(signature){
        if($scope.employee.auth_type === 'Aaw' && !$scope.employee.expiration_na
         && !$scope.employee.auth_expiration) {
            alert('Please provide the expiration date for your work authorization document.');
            return;
        }

        EmploymentProfileService.saveEmploymentAuthByUserId($scope.employee, signature.id)
        .then(function(response){
          $state.go('employee_onboard.tax', { employee_id: $scope.employeeId });
        }, function(error){
          alert('Failed to add employment information');
        });
    };
}]);

var onboardTax = employeeControllers.controller('onboardTax',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   '$window',
   'employeePayrollService',
   'EmployeePreDashboardValidationService',
  function(
    $scope,
    $state,
    $stateParams,
    $location,
    $window,
    employeePayrollService,
    EmployeePreDashboardValidationService){

    $scope.employee = {};
    $scope.employeeId = $stateParams.employee_id;

    EmployeePreDashboardValidationService.onboarding($scope.employeeId, function(){
      $location.path('/employee');
    },
    function(redirectUrl){
      if($location.path() !== redirectUrl){
        $location.path(redirectUrl);
      }
      else{
        $scope.displayAll = true;
      }
    });

    $('body').addClass('onboarding-page');
    $scope.employee.withholdingType = 'single';
    $scope.employee.headOfHousehold = 0;
    $scope.employee.childExpense = 0;


    $scope.calculateTotal = function(){
      employeePayrollService.calculateTotalBasedOnViewW4($scope.employee);
    };

    $scope.userDefinedPointsSet = function(){
      $scope.employee.user_defined_set = true;
    };

    $scope.openW4File = function(){
      if($scope.employee.downloadW4){
        var link = angular.element('#w4doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.submit=function(){
      if(!$scope.employee.downloadW4){
        alert('Please verify you have downloaded and read the entire W-4 form');
        return;
      }
      if(typeof($scope.employee.dependent_count) === 'undefined'){
        alert('Please enter the number of dependents');
        return;
      }
      if(typeof($scope.employee.user_defined_points) === 'undefined'){
        alert('Please enter the final withholding number (line 5 on your W-4)');
        return;
      }
      if(typeof($scope.employee.extra_amount) === 'undefined'){
        $scope.employee.extra_amount = 0;
      }
      var empAuth = employeePayrollService.mapW4ViewToDto($scope.employee);
      employeePayrollService.saveEmployeeTaxByUserId($scope.employeeId, empAuth)
      .then(function(response){
        $state.go('employee_onboard.state_tax', { employee_id: $scope.employeeId });
      });
    };
}]);

var onboardStateTax = employeeControllers.controller('onboardStateTax',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   '$window',
   'EmployeePreDashboardValidationService',
  function(
    $scope,
    $state,
    $stateParams,
    $location,
    $window,
    EmployeePreDashboardValidationService){

    $scope.employeeId = $stateParams.employee_id;

    EmployeePreDashboardValidationService.onboarding($scope.employeeId, function(){
      $location.path('/employee');
    },
    function(redirectUrl){
      if($location.path() !== redirectUrl){
        $location.path(redirectUrl);
      }
      else{
        $scope.displayAll = true;
      }
    });

    $('body').addClass('onboarding-page');

    $scope.onFinish = function(){
      $state.go('employee_onboard.direct_deposit', { employee_id: $scope.employeeId });
    };
}]);

var onboardDirectDeposit = employeeControllers.controller('onboardDirectDeposit',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   '$window',
   'EmployeePreDashboardValidationService',
   'UserOnboardingStepStateService',
  function(
    $scope,
    $state,
    $stateParams,
    $location,
    $window,
    EmployeePreDashboardValidationService,
    UserOnboardingStepStateService){

    $scope.employee = {};
    $scope.userId = $stateParams.employee_id;

    // Direct Deposit directive configurations
    $scope.headerText = 'Add Direct Deposit Account(s) Information';
    $scope.proceed = function(){

      // Mark onboarding step state
      UserOnboardingStepStateService.updateStateByUserAndStep(
        $scope.userId,
        UserOnboardingStepStateService.Steps.DirectDeposit,
        UserOnboardingStepStateService.States.Completed
      );

      $state.go('employee_onboard.document', { employee_id: $scope.userId });
    };

    EmployeePreDashboardValidationService.onboarding($scope.userId, function(){
      $location.path('/employee');
    },
    function(redirectUrl){
      if($location.path() !== redirectUrl){
        $location.path(redirectUrl);
      }
      else{
        $scope.displayAll = true;
      }
    });

    $('body').addClass('onboarding-page');
}]);

var onboardDocument = employeeControllers.controller('onboardDocument',
  ['$scope',
   '$state',
   '$stateParams',
   '$location',
   '$window',
   'EmployeePreDashboardValidationService',
  function(
    $scope,
    $state,
    $stateParams,
    $location,
    $window,
    EmployeePreDashboardValidationService){

    $scope.employee = {};
    $scope.employeeId = $stateParams.employee_id;

    var checkForOnboardingStep = function() {
        EmployeePreDashboardValidationService.onboarding($scope.employeeId, function(){
          $location.path('/employee');
        },
        function(redirectUrl){
          if($location.path() !== redirectUrl){
            $location.path(redirectUrl);
          }
          else{
            $scope.displayAll = true;
          }
        });
    };

    checkForOnboardingStep()

    $('body').addClass('onboarding-page');

    $scope.documentsSigned = function(){
      checkForOnboardingStep();
    };
}]);

var employeeAcceptDocument = employeeControllers.controller('employeeAcceptDocument',
  ['$scope', '$stateParams', '$location', 'DocumentService', 'documentRepository',
  function($scope, $stateParams, $location, DocumentService, documentRepository){
    $scope.employeeId = $stateParams.employee_id;
    $scope.documentId = $stateParams.doc_id;

    var goToOnboarding = function(employeeId){
      $location.path('/employee/onboard/index/' + employeeId);
    };

    $scope.displayAll = true;
    DocumentService.getUserDocumentById($scope.employeeId, $scope.documentId)
      .then(function(doc){
        $scope.curLetter = doc;
      });

    $('body').addClass('onboarding-page');

    $scope.signButtonText = "Sign and Next";

    $scope.allowProceedWithSign = function() {
        return $scope.employee.downloadI9;
    };

    $scope.signDocument = function(signature){
        DocumentService.signUserDocument($scope.curLetter.id, signature.id)
        .then(function(successResponse){
            goToOnboarding($scope.employeeId);
        }, function(failureResponse){
            alert('The signature has not been accepted. The reason is: ' + JSON.stringify(err.data));
        });
    };
  }]);

var employeeBenefitsSignup = employeeControllers.controller(
  'employeeBenefitsSignup',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'BasicLifeInsuranceService',
   'SupplementalLifeInsuranceService',
   'StdService',
   'LtdService',
   'FsaService',
   'HraService',
   'HsaService',
   'CommuterService',
   'ExtraBenefitService',
   'EmployeeBenefitsAvailabilityService',
    function employeeBenefitsSignup(
      $scope,
      $state,
      $stateParams,
      $controller,
      BasicLifeInsuranceService,
      SupplementalLifeInsuranceService,
      StdService,
      LtdService,
      FsaService,
      HraService,
      HsaService,
      CommuterService,
      ExtraBenefitService,
      EmployeeBenefitsAvailabilityService){

      // Inherite scope from base
      $controller('benefitsSignupControllerBase', {$scope: $scope});

      var employeeId = $scope.employeeId;

      $scope.companyPromise.then(function(company) {
        return company.id;
      }).then(function(companyId) {
        return EmployeeBenefitsAvailabilityService.getEmployeeAvailableBenefits(companyId, employeeId)
        .then(function(availableBenefits) {
          if(!availableBenefits){
            alert("You do not have any benefits to enroll. Back to the dashboard page");
            $state.go('/');
          }
          return availableBenefits;
        });
      }).then(function(availableBenefits) {
        $scope.tabs = [];

        if (availableBenefits['medical'] || availableBenefits['dental'] || availableBenefits['vision']){
          $scope.tabs.push({
            "id": 1,
            "heading": "Health Benefits",
            "state":"employee_benefit_signup.health"
          });
        }

        if (availableBenefits['hra']) {
          $scope.tabs.push({
            "id": 2,
            "heading": "HRA",
            "state": "employee_benefit_signup.hra"
          });
        }

        if(availableBenefits['basic_life']) {
          $scope.tabs.push({
            "id": 3,
            "heading": "Basic Life (AD&D)",
            "state":"employee_benefit_signup.basic_life"
          });
        }

        if (availableBenefits['supplemental_life']) {
          $scope.tabs.push({
            "id": 4,
            "heading": "Suppl. Life",
            "state":"employee_benefit_signup.supplemental_life"
          });
        }

        if (availableBenefits['hsa']) {
          $scope.tabs.push({
            "id": 5,
            "heading": "HSA",
            "state": "employee_benefit_signup.hsa"
          });
        }

        if (availableBenefits['fsa']) {
          $scope.tabs.push({
            "id": 6,
            "heading": "FSA",
            "state": "employee_benefit_signup.fsa"
          });
        }

        if (availableBenefits['std']) {
          $scope.tabs.push({
            "id": 7,
            "heading": "STD",
            "state": "employee_benefit_signup.std"
          });
        }

        if (availableBenefits['ltd']) {
          $scope.tabs.push({
            "id": 8,
            "heading": "LTD",
            "state": "employee_benefit_signup.ltd"
          });
        }

        if (availableBenefits['commuter']) {
          $scope.tabs.push({
            "id": 9,
            "heading": "Commuter",
            "state": "employee_benefit_signup.commuter"
          });
        }

        if (availableBenefits['extra']) {
          $scope.tabs.push({
            "id": 10,
            "heading": "Extra Benefits",
            "state": "employee_benefit_signup.extra_benefit"
          });
        }

        // Summary tab not needed when no benefits available
        if ($scope.tabs.length > 0) {
          $scope.tabs.push({
            "id": 11,
            "heading": "Summary",
            "state": "employee_benefit_signup.summary"
          });
        }

        // Always default to set the first tab be active.
        if ($scope.tabs.length > 0) {
          $scope.tabs[0].active = true;
          $scope.hasBenefits = true;
        }
      });

      $scope.go_to_state = function(state) {
        $state.go(state);
        for (i = 0; i < $scope.tabs.length; i++) {
          $scope.tabs[i].active = ($scope.tabs[i].state === state);
        }
      };

      $scope.addMember = function(){
        $state.go('employee_family', { employeeId:employeeId });
      };

      // TODO:
      // This is the call back the confirm-unsaved-on-exit can call up on
      // selection of "cancel".
      // Could there a be a less "by convention" way of doing this? Could
      // we somehow pass a callback into the directive?
      $scope.state_exit_cancelled = function(originalState) {
        for (i = 0; i < $scope.tabs.length; i++) {
          $scope.tabs[i].active = ($scope.tabs[i].state === originalState.name);
        }
      }

    }]);

var healthBenefitsSignup = employeeControllers.controller(
  'healthBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   '$modal',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'PersonService',
   'benefitDisplayService',
   'FsaService',
   'BasicLifeInsuranceService',
   'HealthBenefitsService',
    function healthBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      $modal,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      PersonService,
      benefitDisplayService,
      FsaService,
      BasicLifeInsuranceService,
      HealthBenefitsService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var medicalPlans = [];
        var dentalPlans = [];
        var visionPlans = [];
        var employeeId = $scope.employeeId;
        $scope.employee_id = employeeId;
        $scope.availablePlans = [];
        $scope.family = [];
        $scope.selectedBenefits =[];
        $scope.selectedBenefitHashmap = {};

        var getEligibleFamilyMember = function(benefit, selected){
          var availFamilyList = {};
          var selectedMemberHash = {};
          if(selected)
          {
            _.each(selected.enrolleds, function(enrolled){
              enrolled.person.pcp = enrolled.pcp;
              selectedMemberHash[enrolled.person.id] = enrolled.person;
            });
          }
          switch(benefit.benefit_option_type)
          {
            case 'individual':
              availFamilyList.familyList = _.where(angular.copy($scope.family), {relationship:'self'});
              availFamilyList.eligibleNumber = 1;
              availFamilyList.minimumRequired = 1;
            break;
            case 'individual_plus_spouse':
              availFamilyList.familyList = _.filter(angular.copy($scope.family), function(elem){
                return elem.relationship == 'self'
                    || elem.relationship == 'spouse'
                    || elem.relationship == 'ex-spouse'
                    || elem.relationship == 'life partner'
                });
              availFamilyList.eligibleNumber = 2;
              availFamilyList.minimumRequired = 2;
            break;
            case 'individual_plus_one':
              availFamilyList.familyList = angular.copy($scope.family);
              availFamilyList.eligibleNumber = 2;
              availFamilyList.minimumRequired = 2;
            break;
            case 'individual_plus_children':
              availFamilyList.familyList = _.filter(angular.copy($scope.family), function(elem){
                return elem.relationship == 'self'
                    || elem.relationship == 'dependent'
                    || elem.relationship == 'child'
                    || elem.relationship == 'stepchild'
                });
              availFamilyList.eligibleNumber = $scope.family.length;
              availFamilyList.minimumRequired = 2;
            break;
            default:
            case 'family':
            case 'individual_plus_family':
              availFamilyList.familyList = angular.copy($scope.family);
              availFamilyList.eligibleNumber = $scope.family.length;
              availFamilyList.minimumRequired = 2;
            break;
          }
          _.each(availFamilyList.familyList, function(member){
            if(selectedMemberHash[member.id])
            {
              member.selected = true;
            }
          });
          return availFamilyList;
        };

        PersonService.getFamilyInfo(employeeId)
        .then(function(family){
          _.each(family, function(member){
            member.ticked = false;
            $scope.family.push(member);
          });

          $scope.companyPromise.then(function(company){

            benefitDisplayService.getHealthBenefitsForDisplay(company, false, $scope.userCompanyGroupId)
            .then(function(healthBenefitToDisplay){
              $scope.medicalBenefitGroup = healthBenefitToDisplay.medicalBenefitGroup;
              $scope.nonMedicalBenefitArray = healthBenefitToDisplay.nonMedicalBenefitArray;
              $scope.benefitCount = healthBenefitToDisplay.benefitCount;
            });

            //First get all the enrolled benefit list
            employeeBenefits.enroll().get({userId:employeeId, companyId:company.id})
              .$promise.then(function(response){
                $scope.selectedBenefits = response.benefits;
                _.each($scope.selectedBenefits, function(benefitMember){
                  benefitMember.benefit.pcp = benefitMember.pcp;
                  $scope.selectedBenefitHashmap[benefitMember.benefit.id] = benefitMember.benefit;

                  // Need to pass PCP number from enrolled to family object
                  _.each(benefitMember.enrolleds, function(enrolled){
                    var member = _.find($scope.family, function(familyMember){
                      return familyMember.id === enrolled.person.id;
                    });
                    if (member && !member.pcp){
                      member.pcp = enrolled.pcp;
                    }
                  })
                });

                //Then get all the waived list
                employeeBenefits.waive().query({userId:employeeId})
                  .$promise.then(function(response){
                    $scope.waivedBenefits = _.filter(response, function(waived){
                      return waived.company.id == company.id;
                    });


                    //Then get all the benefits associated with the company
                    HealthBenefitsService.getPlansForCompanyGroup(company.id, $scope.userCompanyGroupId)
                    .then(function(availableBenefits){
                      _.each(availableBenefits, function(availBenefit){
                        var benefitFamilyPlan = { 'benefit': availBenefit};
                        var selectedBenefitPlan = _.first(_.filter($scope.selectedBenefits, function(selectedBen){
                          return selectedBen.benefit.benefit_plan.id == availBenefit.benefit_plan.id;
                        }));

                        benefitFamilyPlan.eligibleMemberCombo = getEligibleFamilyMember(availBenefit, selectedBenefitPlan);
                        var benefitType = availBenefit.benefit_plan.benefit_type.name;
                        var curTypePlan = _.find($scope.availablePlans, function(plans){
                          var hit = _.find(plans.benefitList, function(benefit){
                            return benefit.benefit.benefit_plan.benefit_type.name == benefitType;
                          });
                          if (hit){
                            return true;
                          }
                          return false;
                        })
                        if(!curTypePlan)
                        {
                          curTypePlan = {type:availBenefit.benefit_plan.benefit_type, benefitList:[]};

                          var waiveOption = {
                                              benefit: {
                                                id:-1,
                                                benefit_plan: {
                                                  name: 'Waive',
                                                  employee_cost_per_period: 0,
                                                  benefit_type: {
                                                    name: availBenefit.benefit_type
                                                  }
                                                },
                                                employee_cost_per_period: 0,
                                                benefit_option_type: 'all'
                                              }
                                            };
                          curTypePlan.benefitList.push(waiveOption);
                          $scope.availablePlans.push(curTypePlan);
                        }
                        curTypePlan.benefitList.push(benefitFamilyPlan);
                        curTypePlan.benefit_type = benefitType;
                      });

                      //Now match the selected with the actual benefit plan(medical, dental, vision)
                      _.each($scope.availablePlans, function(typedPlan){
                        _.each(typedPlan.benefitList, function(curBenefit){
                          var retrievedBenefit = $scope.selectedBenefitHashmap[curBenefit.benefit.id];
                          if(retrievedBenefit){
                            typedPlan.selected = curBenefit;
                            typedPlan.selected.pcp = retrievedBenefit.pcp;
                          }
                        });
                        if(!typedPlan.selected){
                          //Now, we cannot find a selected benefit plan.
                          //check if it is waived.
                          var waivedBenefitOfType = _.find($scope.waivedBenefits, function(waived){
                            return waived.benefit_type.id == typedPlan.type.id;
                          });
                          if(waivedBenefitOfType){
                            typedPlan.selected = _.find(typedPlan.benefitList, function(benefitMember){
                              return benefitMember.benefit.id == -1;
                            });
                            typedPlan.selected.benefit.reason = waivedBenefitOfType.reason;
                          }

                        }
                      });
                    });
                  });
            });
          });
        });

        $scope.preSelectEmployee = function(selectedBenefitPlan) {
          if (selectedBenefitPlan &&
              selectedBenefitPlan.eligibleMemberCombo &&
              selectedBenefitPlan.eligibleMemberCombo.familyList){
            var self = _.findWhere(selectedBenefitPlan.eligibleMemberCombo.familyList, {relationship: 'self'});
            self.selected = true;
          }
        };

        $scope.memberSelected = function(selectedBenefitFamily, member){
          var selectedMemberList = _.where(selectedBenefitFamily.eligibleMemberCombo.familyList, {selected:true});
          if(selectedMemberList.length > selectedBenefitFamily.eligibleMemberCombo.eligibleNumber){
            alert("You can only select " + selectedBenefitFamily.eligibleMemberCombo.eligibleNumber + ' family member(s)');
            member.selected = false;
          }
          var self = _.findWhere(selectedMemberList, {relationship:'self'});
          if(selectedMemberList.length > 0 && !self)
          {
            alert("You cannot select other family member without select yourself first!");
            member.selected = member.relationship == 'self';
          }
        };

        $scope.isMedicalBenefitType = function(benefit){
          return benefit && benefit.benefit_type === 'Medical';
        };

        $scope.isWaived = function(selectedPlan){
          if (!selectedPlan ||!selectedPlan.benefit){
            return true;
          }
          return selectedPlan.benefit.id === -1;
        };

        $scope.medicalWaiveReasons = [
          'I am covered under another plan as a spouse or dependent',
          'I am covered by MassHealth, Medicare, Commonwealth Health Connector plan, non-group, or Veterans program',
          'I am covered under another plan sponsored by a second employer',
          'I am covered by another health plan sponsored by this employer'
        ];

        $scope.save = function(){
          var invalid = false;
          var saveRequest = {benefits:[],waived:[]};
          var invalidEnrollNumberList = [];
          var noPCPError = false;
          var hasEmptyRequiredPCP = false;

          $scope.companyPromise.then(function(company){

            _.each($scope.availablePlans, function(benefitTypePlan){
              var enrolledList = [];
              if (typeof benefitTypePlan.selected.eligibleMemberCombo != 'undefined'){
                _.each(benefitTypePlan.selected.eligibleMemberCombo.familyList, function(member){
                  if(member.selected)
                  {
                    if(!benefitTypePlan.selected.benefit.benefit_plan.mandatory_pcp){
                      member.pcp = undefined;
                    }
                    else if(!hasEmptyRequiredPCP && !member.pcp){
                      hasEmptyRequiredPCP = true;
                    }
                    enrolledList.push({id:member.id, pcp:member.pcp});
                  }
                });
              }

              if(enrolledList.length > 0)
              {
                var requestBenefit = {
                  benefit:{
                    id:benefitTypePlan.selected.benefit.id,
                    benefit_type:benefitTypePlan.selected.benefit.benefit_plan.benefit_type.name
                  },
                  enrolleds:enrolledList
                };
                saveRequest.benefits.push(requestBenefit);

                if(requestBenefit.enrolleds.length < benefitTypePlan.selected.eligibleMemberCombo.minimumRequired)
                {
                  //validation failed.
                  var invalidEnrollNumber = {};
                  invalidEnrollNumber.name = benefitTypePlan.selected.benefit.benefit_plan.name;
                  invalidEnrollNumber.requiredNumber = benefitTypePlan.selected.eligibleMemberCombo.minimumRequired;
                  invalidEnrollNumberList.push(invalidEnrollNumber);
                }
              }
            });

            if(invalidEnrollNumberList.length > 0){
              alert("For benefit " + invalidEnrollNumberList[0].name +
                      ", you have to elect at least" + invalidEnrollNumberList[0].requiredNumber + " family members!");
              return;
            }

            if(hasEmptyRequiredPCP){
              alert("The benefit plan you selected requires PCP number. Please confirm you have proviced correct number.");
              return;
            }

            saveRequest.waivedRequest = {company:company.id, waived:[]};
            _.each($scope.availablePlans, function(benefitPlan){
              if (benefitPlan.selected.benefit && benefitPlan.selected.benefit.benefit_plan.name === 'Waive'){
                if (benefitPlan.benefit_type === 'Medical' && !benefitPlan.selected.benefit.reason){
                  alert("Please select a reason to waive medical plan.");
                  invalid = true;
                  return;
                }

                var type = benefitPlan.benefit_type;
                var waiveReason = 'Not applicable';
                //This code below is such an hack. We need to get the type key from the server!
                //CHANGE THIS
                var typeKey = 0;
                if (type === 'Medical'){
                  typeKey = 1;
                  waiveReason = benefitPlan.selected.benefit.reason;
                }
                if (type === 'Dental'){
                  typeKey = 2;
                }
                if (type === 'Vision'){
                  typeKey = 3;
                }
                saveRequest.waivedRequest.waived.push({benefit_type: typeKey, type_name: type, reason: waiveReason});
              }
            });

            if (invalid) {
              return;
            }

            console.log(saveRequest);

            // Compose the update reason and attach it to the requests
            var updateReason = {
                "record_reason_id": $scope.updateReason.selectedReason.id,
                "record_reason_note": $scope.updateReason.notes
            };

            if (!$scope.updateReason.notes) {
              updateReason.record_reason_note = '';
            }

            saveRequest.waivedRequest.record_reason = updateReason;
            employeeBenefits.waive().save({userId: employeeId}, saveRequest.waivedRequest, function(){},
            function(errorResponse){
              alert('Saving waived selection failed because: ' + errorResponse.data);
              $scope.savedSuccess = false;
            });

            saveRequest.record_reason = updateReason;
            employeeBenefits.enroll().save({userId: employeeId, companyId: company.id}, saveRequest, function(){
                var modalInstance = $scope.showSaveSuccessModal();
                modalInstance.result.then(function(){
                    $scope.transitionToNextTab($scope.tabs);
                });
                $scope.myForm.$setPristine();
            }, function(){
              $scope.savedSuccess = false;
            });

          });
        };

        $scope.benefit_type = 'Health Benefits';

        $scope.openPlanDetailsModal = function() {
            $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_health_plan.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };
    }]);

var fsaBenefitsSignup = employeeControllers.controller(
  'fsaBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   '$modal',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'FsaService',
   'BasicLifeInsuranceService',
    function fsaBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      $modal,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      FsaService,
      BasicLifeInsuranceService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        // FSA election data
        $scope.fsaUpdateReasons = [
          { text: 'Please make a selection...', value: 0 },
          { text: 'Waive FSA plan', value: 1 },
          { text: 'New Enrollment or annual enrollment changes', value: 2 },
          { text: 'Dependent care cost provider changes', value: 3 },
          { text: 'Dependent satisfies or ceases to satisfy dependent eligibility requirements', value: 4 },
          { text: 'Birth/Death of spouse or dependent, adoption or placement for adoption', value: 5 },
          { text: 'Spouse\'s employment commenced/terminated', value: 6 },
          { text: 'Status change from full-time to part-time or vice versa by employee or spouse', value: 7 },
          { text: 'Eligibility or Ineligibility of Medicare/Medicaid', value: 8 },
          { text: 'Change from salaried to hourly or vice versa', value: 9 },
          { text: 'Marriage/Divorce/Legal Separation', value: 10 },
          { text: 'Unpaid leave of absence by employee or spouse', value: 11 },
          { text: 'Return from unpaid leave of absence by employee or spouse', value: 12 }
        ];

        $scope.companyPromise.then(function(company) {
          FsaService.getFsaPlanForCompanyGroup($scope.userCompanyGroupId).then(function(fsaPlanForCompany) {
            // Current implementation implies one company will only have one FSA plan.
            // If use case changes in the future, we need to update the employee signup flow.
            $scope.fsaPlan = fsaPlanForCompany[0];
          });

          // Get current user selection
          FsaService.getFsaElectionForUser(employeeId, company.id)
          .then(function(response) {
              $scope.fsaElection = response;
              if (response.update_reason && response.update_reason.length > 0){
                $scope.selectedFsaUpdateReason = _.findWhere($scope.fsaUpdateReasons, {text: response.update_reason});
              } else{
                $scope.selectedFsaUpdateReason = $scope.fsaUpdateReasons[0];
              }
            });
        });

        $scope.waivedFsa = function() {
          return $scope.selectedFsaUpdateReason && $scope.selectedFsaUpdateReason.value === 1;
        };

        $scope.openPlanDetailsModal = function(){
          $scope.fsaPlanModal = $scope.fsaPlan;
          $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_fsa_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

        // Whether the user has selected a reason for updating
        // his/her FSA configuration.
        $scope.isFsaUpdateReasonSelected = function() {
          return $scope.selectedFsaUpdateReason && $scope.selectedFsaUpdateReason.value > 0;
        };

        $scope.isValidToSave = function() {
            return $scope.isFsaUpdateReasonSelected()
                && !$scope.myForm.$invalid;
        };

        $scope.save = function(){
          // Save FSA selection if user specifies a reason
          if ($scope.isFsaUpdateReasonSelected()){
            $scope.fsaElection.update_reason = $scope.selectedFsaUpdateReason.text;
            $scope.fsaElection.company_fsa_plan = $scope.fsaPlan.companyPlanId;
          }
          else{
            $scope.savedSuccess = false;
            return;
          }

          // Set values to NULL if user chooses to waive FSA plan
          if ($scope.selectedFsaUpdateReason.value === 1) {
            $scope.fsaElection.update_reason = $scope.selectedFsaUpdateReason.text;
            $scope.fsaElection.company_fsa_plan = null;
            $scope.fsaElection.primary_amount_per_year = null;
            $scope.fsaElection.dependent_amount_per_year = null;
          }

          FsaService.saveFsaElection($scope.fsaElection, $scope.updateReason
            , function() {
                  var modalInstance = $scope.showSaveSuccessModal();
                  modalInstance.result.then(function(){
                      $scope.transitionToNextTab($scope.tabs);
                  });
                  $scope.myForm.$setPristine();
            }
            , function() {
                $scope.savedSuccess = false;
            });
        };

        $scope.benefit_type = 'FSA'
    }]);

var hsaBenefitSignup = employeeControllers.controller(
  'hsaBenefitSignup',
  ['$scope',
   '$controller',
   '$modal',
   'HsaService',
    function hraBenefitsSignup(
      $scope,
      $controller,
      $modal,
      HsaService){

    // Inherite scope from base
    $controller('benefitsSignupControllerBase', {$scope: $scope});

    var employeeId = $scope.employeeId;
    var groupId = $scope.userInfo.user.company_group_user[0].company_group.id;

    HsaService.GetHsaPlanByCompanyGroup(groupId).then(function(hsaPlans) {
      if (hsaPlans.length > 0) {
        $scope.hsaPlan = hsaPlans[0];
      }
      else
      {
        throw new Error('Did not locate active company HSA plans!');
      }
    });

    HsaService.GetHsaPlanEnrollmentByUser(employeeId).then(function(personPlan) {
      $scope.personPlan = personPlan;
      // If HRA has been waived, uncheck the checkbox
      if (personPlan.id && !personPlan.company_hsa_plan) {
        $scope.personPlan.enrollHsa = false;
      } else {
        $scope.personPlan.enrollHsa = true;
      }
    }, function(error) {
      if (error.status === 404) {
        $scope.personPlan = {"enrollHsa": false};
      }
    });

    $scope.save = function() {
      // Save plan selection
      HsaService.SaveHsaPlanForEmployee(employeeId, $scope.hsaPlan, $scope.personPlan, $scope.updateReason)
      .then(function() {
          var modalInstance = $scope.showSaveSuccessModal();
          modalInstance.result.then(function(){
              $scope.transitionToNextTab($scope.tabs);
          });
          $scope.myForm.$setPristine();
        }
        , function(error) {
          alert('Failed to save your benefits election. Please try again later.');
        }
      );
    };

    $scope.openPlanDetailsModal = function() {
        $scope.detailsModalCompanyPlanToDisplay = $scope.companyPlan;
        $modal.open({
          templateUrl: '/static/partials/benefit_selection/modal_hra_plan_details.html',
          controller: 'planDetailsModalController',
          size: 'lg',
          scope: $scope
        });
    };
  }
]);

var basicLifeBenefitsSignup = employeeControllers.controller(
  'basicLifeBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   '$modal',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'FsaService',
   'BasicLifeInsuranceService',
    function basicLifeBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      $modal,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      FsaService,
      BasicLifeInsuranceService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.companyPromise.then(function(company){
          BasicLifeInsuranceService.getBasicLifeInsurancePlansForCompanyGroup(company, $scope.userCompanyGroupId).then(function(plans) {

            if (plans.length > 0) {
              $scope.basicLifeInsurancePlan = {};
              $scope.basicLifeInsurancePlan.currentUserId = employeeId;
              $scope.basicLifeInsurancePlan.selected = true;
              $scope.basicLifeInsurancePlan.mandatory = true;
              // Ideally, basicLifeInsurancePlan should be user basic life insurance plan
              // plans returned here are company life insurance plan, which should be a property of
              // the basicLifeInsurancePlan rather than make the two parallel.
              $scope.basicLifeInsurancePlan.companyLifeInsurancePlan = plans[0];

              // Calculate employee premium for basic life insurance benefit
              BasicLifeInsuranceService.getLifeInsuranceEmployeePremium(employeeId, plans[0]).then(function(premium) {
                $scope.basicLifeInsurancePlan.employee_cost_per_period = premium.employee;

                if (parseFloat($scope.basicLifeInsurancePlan.employee_cost_per_period) > 0){
                  $scope.basicLifeInsurancePlan.mandatory = false;
                }
              });
            }

            // Get current user's basic life insurance plan situation
            BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employeeId, company).then(function(userPlan){
              if (userPlan === undefined) {
                // TODO:
                // The user (now) belongs to a group that does not provide
                // benefit.
                // Our current behavior is to not even show the tab when no
                // company plan is available, so users would not even get
                // here (they don't see the tab, and cannot save the plan)
                // But we might need to revisit, in general, what to do when
                // company (group) plans removed, where users have been previously
                // registered to.
                alert("System found no available plans to enroll!");
                return;
              }

              if (userPlan.selected) {
                $scope.basicLifeInsurancePlan.enrolled = true;
                $scope.basicLifeInsurancePlan.id = userPlan.id;
              }
              else {
                $scope.basicLifeInsurancePlan.enrolled = false;
              }

              $scope.basicLifeInsurancePlan.life_insurance_beneficiary = userPlan.life_insurance_beneficiary;
              $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary = userPlan.life_insurance_contingent_beneficiary;
            }, function(error){
              $scope.error = true;
            });

          });
        });

        $scope.addBeneficiaryToBasic = function(){
          if (!$scope.basicLifeInsurancePlan.life_insurance_beneficiary){
            $scope.basicLifeInsurancePlan.life_insurance_beneficiary = []
          }
          $scope.basicLifeInsurancePlan.life_insurance_beneficiary.push({});
        };

        $scope.addContingentBeneficiaryToBasic = function(){
          if (!$scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary){
            $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary = []
          }
          $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary.push({});
        };

        $scope.removeFromList = function(item, list){
          var index = list.indexOf(item);
          list.splice(index, 1);
        };

        $scope.openPlanDetailsModal = function(){
          $scope.companyBasicLifeToDisplay = $scope.basicLifeInsurancePlan;
          $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_basic_life_plan_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

        $scope.save = function(){

          ///////////////////////////////////////////////////////////////////////////
          // Save basic life insurance
          // TO-DO: Need to better organize the logic to save basic life insurance
          ///////////////////////////////////////////////////////////////////////////
          BasicLifeInsuranceService.saveBasicLifeInsurancePlanForUser($scope.basicLifeInsurancePlan, $scope.updateReason
            , function() {
              var modalInstance = $scope.showSaveSuccessModal();
              modalInstance.result.then(function(){
                $scope.transitionToNextTab($scope.tabs);
              });
              $scope.myForm.$setPristine();
            }
            , function(error){
              $scope.savedSuccess = false;
              alert('Failed to save basic life insurance. Please make sure all required fields have been filled.')
            });
        };

        $scope.benefit_type = 'Basic Life Insurance';
    }]);

var supplementalLifeBenefitsSignup = employeeControllers.controller(
  'supplementalLifeBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   '$modal',
   'SupplementalLifeInsuranceService',
   'SupplementalLifeInsuranceConditionService',
   'PersonService',
   'UserService',
   'CompanyFeatureService',
    function supplementalLifeBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      $modal,
      SupplementalLifeInsuranceService,
      SupplementalLifeInsuranceConditionService,
      PersonService,
      UserService,
      CompanyFeatureService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        SupplementalLifeInsuranceConditionService.getConditions().then(function(conditions){
            $scope.conditions = conditions;
        });

        $scope.familyInfo={};
        PersonService.getFamilyInfo($scope.employeeId)
        .then(function(family){
          _.each(family, function(member){
            if(member.relationship === 'self'){
                $scope.familyInfo.selfPerson = member;
            }
            // Assume a person can only have either a spouse OR a life partner
            else if (member.relationship === 'spouse' || member.relationship === 'life partner')
            {
                $scope.familyInfo.spousePerson = member;
            }
            else{
              $scope.familyInfo.hasChild = true;
            }
          });
        });

        $scope.companyPlans = [ { text: '<Waive Supplemental Life Insurance>', value: null } ];

        $scope.companyPromise.then(function(company){
          SupplementalLifeInsuranceService.getPlansForCompanyGroup($scope.userCompanyGroupId).then(function(plans) {

            // Populate available company plans
            _.each(plans, function(plan) {
              $scope.companyPlans.push({ text: plan.planName, value: plan });
            });

            // Get current user's plan situation
            SupplementalLifeInsuranceService.getPlanByUser(employeeId, company, true).then(function(plan) {
                // It is guaranteed there is a plan returned, as the call above
                // asks the service to return a blank plan if non-existing plan
                // enrollments found.
                $scope.supplementalLifeInsurancePlan = plan;

                // Figure out the right option to select, based on the
                // current company plan bound to the person plan in scope
                var optionToSelect = _.find($scope.companyPlans, function(option) {
                    return option.value && option.value.companyPlanId === $scope.supplementalLifeInsurancePlan.companyPlanId;
                });

                if (optionToSelect) {
                  $scope.selectedCompanyPlan = optionToSelect;
                }
                else {
                  // Default to "waived" selection, as the person does not have a plan
                  // enrollment yet.
                  $scope.selectedCompanyPlan = $scope.companyPlans[0];
                }

                // "Translate" condition to a more easily presentable/manipulatable property
                $scope.supplementalLifeInsurancePlan.selfUseTobacco = $scope.supplementalLifeInsurancePlan.selfPlanCondition != null
                    && $scope.supplementalLifeInsurancePlan.selfPlanCondition.name === 'Tobacco';

                $scope.supplementalLifeInsurancePlan.spouseUseTobacco = $scope.supplementalLifeInsurancePlan.spousePlanCondition != null
                    && $scope.supplementalLifeInsurancePlan.spousePlanCondition.name === 'Tobacco';
            });

            UserService.getCurrentRoleCompleteFeatureStatus().then(function(allFeatureStatus) {
                $scope.allFeatureStatus = allFeatureStatus;
            });
          });
        });

        // User should be able to add up to 4 beneficiaries of life insurance
        $scope.addMainBeneficiary = function(){
          $scope.supplementalLifeInsurancePlan.beneficiaryList.mainBeneficiaries.push({
            'beneficiaryTier': '1'
          });
        };

        $scope.addContingentBeneficiary = function(){
          $scope.supplementalLifeInsurancePlan.beneficiaryList.contingentBeneficiaries.push({
            'beneficiaryTier': '2'
          });
        };

        $scope.removeMainBeneficiary = function(beneficiary){
          var index = $scope.supplementalLifeInsurancePlan.beneficiaryList.mainBeneficiaries.indexOf(beneficiary);
          $scope.supplementalLifeInsurancePlan.beneficiaryList.mainBeneficiaries.splice(index, 1);
        };

        $scope.removeContingentBeneficiary = function(beneficiary){
          var index = $scope.supplementalLifeInsurancePlan.beneficiaryList.contingentBeneficiaries.indexOf(beneficiary);
          $scope.supplementalLifeInsurancePlan.beneficiaryList.contingentBeneficiaries.splice(index, 1);
        };

        // Whether the user selected to waive life insurance
        $scope.isWaiveBenefitSelected = function() {
          return !$scope.selectedCompanyPlan.value;
        };

        $scope.isValidCompanyPlanSelected = function() {
            return $scope.selectedCompanyPlan && !$scope.isWaiveBenefitSelected();
        };

        $scope.computeAgeFromBirthDate = function(birthDate) {
            return moment().diff(birthDate, 'year');
        };

        $scope.getSelfRateInfo = function() {
            if (!$scope.familyInfo.selfPerson) {
                return null;
            }

            var age = $scope.computeAgeFromBirthDate($scope.familyInfo.selfPerson.birth_date);

            var combinedRate = _.find(
                $scope.selectedCompanyPlan.value.planRates.employeeRateTable,
                function(rateRow) {
                    return rateRow.ageMin <= age && rateRow.ageMax >= age;
                });

            if (!combinedRate) {
                return null;
            }

            return {
                'benefitReductionPercentage' : combinedRate.benefitReductionPercentage,
                'rate' : $scope.supplementalLifeInsurancePlan.selfUseTobacco
                            ? combinedRate.tobaccoRate.ratePer10000
                            : combinedRate.nonTobaccoRate.ratePer10000
            };
        }

        $scope.getSpouseRateInfo = function() {
            if (!$scope.familyInfo.spousePerson) {
                return null;
            }

            // For spouse rate calculation, respect the flag set on the plan
            // about whether to use employee birth date for spouse.
            var age = $scope.computeAgeFromBirthDate(
                $scope.selectedCompanyPlan.value.useEmployeeAgeForSpouse
                    ? $scope.familyInfo.selfPerson.birth_date
                    : $scope.familyInfo.spousePerson.birth_date);

            var combinedRate = _.find(
                $scope.selectedCompanyPlan.value.planRates.spouseRateTable,
                function(rateRow) {
                    return rateRow.ageMin <= age && rateRow.ageMax >= age;
                });

            if (!combinedRate) {
                return null;
            }

            return {
                'benefitReductionPercentage' : combinedRate.benefitReductionPercentage,
                'rate' : $scope.supplementalLifeInsurancePlan.spouseUseTobacco
                    ? combinedRate.tobaccoRate.ratePer10000
                    : combinedRate.nonTobaccoRate.ratePer10000
            };
        };

        $scope.getChildRate = function() {
            if (!$scope.familyInfo.hasChild) {
                return null;
            }
            return $scope.selectedCompanyPlan.value.planRates.childRate.ratePer10000;
        };

        $scope.getPremiumForDisplay = function(premium){
            if (premium == null) {
                return null;
            }

            return premium.toFixed(2);
        };

        var getPremiumForStore = function(premium){
            if (premium == null) {
                return null;
            }

            return premium.toFixed(10);
        };

        //TODO: We need to move the calculation below to service level, Not controller level
        $scope.computeSelfPremium = function() {
            // Refresh the local cached copy of self rate info
            $scope.selfRateInfo = $scope.getSelfRateInfo();
            if (!$scope.selfRateInfo) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.selfElectedAmount
                    * (1.0 - $scope.selfRateInfo.benefitReductionPercentage / 100.0) / 10000 * $scope.selfRateInfo.rate;
            return premium;
        };

        //TODO: We need to move the calculation below to service level, Not controller level
        $scope.computeSpousePremium = function() {
            // Refresh the local cached copy of self rate info
            $scope.spouseRateInfo = $scope.getSpouseRateInfo();
            if (!$scope.spouseRateInfo) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.spouseElectedAmount
                   * (1.0 - $scope.spouseRateInfo.benefitReductionPercentage / 100.0) / 10000 * $scope.spouseRateInfo.rate;
            return premium;
        };

        //TODO: We need to move the calculation below to service level, Not controller level
        $scope.computeChildPremium = function() {
            var rate = $scope.getChildRate();
            if (!rate) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.childElectedAmount / 10000 * rate;
            return premium;
        }

        $scope.computeSelfAdadPremium = function() {
            if ($scope.supplementalLifeInsurancePlan.enrollAdadSelf) {
                return 0;
            }
            return null;
        };
        $scope.computeSpouseAdadPremium = function() {
            if ($scope.supplementalLifeInsurancePlan.enrollAdadSpouse) {
                return 0;
            }
            return null;
        };
        $scope.computeChildAdadPremium = function() {
            if ($scope.supplementalLifeInsurancePlan.enrollAdadChild) {
                return 0;
            }
            return null;
        };

        $scope.save = function(){
          // Save life insurance
          if ($scope.isWaiveBenefitSelected()) {

            // Set company plan id to null when user choose to waive
            $scope.supplementalLifeInsurancePlan.companyPlanId = null;
          } else {
            $scope.supplementalLifeInsurancePlan.companyPlanId = $scope.selectedCompanyPlan.value.companyPlanId;

            // Translate convenient view model properties back to the proper nested
            // members
            $scope.supplementalLifeInsurancePlan.selfPlanCondition = $scope.supplementalLifeInsurancePlan.selfUseTobacco
                                                                        ? $scope.conditions['Tobacco']
                                                                        : $scope.conditions['Non-Tobacco'];

            $scope.supplementalLifeInsurancePlan.spousePlanCondition = $scope.supplementalLifeInsurancePlan.spouseUseTobacco
                                                                        ? $scope.conditions['Tobacco']
                                                                        : $scope.conditions['Non-Tobacco'];

            // Persists the premium calculations
            $scope.supplementalLifeInsurancePlan.selfPremiumPerMonth = getPremiumForStore($scope.computeSelfPremium());
            $scope.supplementalLifeInsurancePlan.spousePremiumPerMonth = getPremiumForStore($scope.computeSpousePremium());
            $scope.supplementalLifeInsurancePlan.childPremiumPerMonth = getPremiumForStore($scope.computeChildPremium());

            // Persists the premium for AD&D
            $scope.supplementalLifeInsurancePlan.selfAdadPremiumPerMonth = getPremiumForStore($scope.computeSelfAdadPremium());
            $scope.supplementalLifeInsurancePlan.spouseAdadPremiumPerMonth = getPremiumForStore($scope.computeSpouseAdadPremium());
            $scope.supplementalLifeInsurancePlan.childAdadPremiumPerMonth = getPremiumForStore($scope.computeChildAdadPremium());
          }

          SupplementalLifeInsuranceService.savePersonPlan($scope.supplementalLifeInsurancePlan, $scope.updateReason).then (
            function() {
              var modalInstance = $scope.showSaveSuccessModal();
              modalInstance.result.then(function(){
                $scope.transitionToNextTab($scope.tabs);
              });
              $scope.myForm.$setPristine();
            }
            , function(error) {
              alert('Failed to save your beneficiary information. Please make sure all required fields have been filled.');
            });
        };

        $scope.openPlanDetailsModal = function() {
            $scope.detailsModalCompanyPlanToDisplay = $scope.selectedCompanyPlan.value;
            $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_supplemental_life_plan_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

        $scope.benefit_type = 'Supplemental Life Insurance';

        $scope.isAdadEnabled = function() {
            return $scope.allFeatureStatus 
                && $scope.allFeatureStatus.isFeatureEnabled(
                    CompanyFeatureService.AppFeatureNames.ADAD);
        };

    }]);

var stdBenefitsSignup = employeeControllers.controller(
  'stdBenefitsSignup',
  ['$scope',
   '$controller',
   '$modal',
   'StdService',
    function stdBenefitsSignup(
      $scope,
      $controller,
      $modal,
      StdService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.enrollBenefits = true;

        $scope.showSelectAmount = function() {
          return $scope.companyStdPlan &&
            $scope.companyStdPlan.allowUserSelectAmount &&
            $scope.enrollBenefits;
        };

        $scope.calculatePremium = function(amount) {
          StdService.getTotalPremiumForUserCompanyStdPlan(
            $scope.employeeId, $scope.companyStdPlan, amount)
          .then(function(premiumInfo) {
            $scope.companyStdPlan.totalPremium = premiumInfo.totalPremium;
            $scope.companyStdPlan.employeePremium = premiumInfo.employeePremiumPerPayPeriod;
            $scope.companyStdPlan.effectiveBenefitAmount = premiumInfo.effectiveBenefitAmount;
          }, function(error){
            alert("Could not get premium info. Error is: " + error);
            $scope.companyStdPlan.totalPremium = 0;
            $scope.companyStdPlan.employeePremium = 0;
          });
        };

        $scope.hasPremium = function(premium) {
          var premiumNumber = parseFloat(premium);
          return _.isNumber(premiumNumber);
        };

        $scope.companyPromise.then(function(company){
          $scope.company = company;
        });

        StdService.getStdPlansForCompanyGroup($scope.userCompanyGroupId)
        .then(function(stdPlans) {
          // For now, similar to basic life, simplify the problem space by
          // taking the first available plan for the company.
          if (stdPlans.length > 0) {
              $scope.companyStdPlan = stdPlans[0];
              return $scope.companyStdPlan;
          }
          return {};
        }).then(function(stdPlan) {
          if (!$scope.companyStdPlan) {
            $scope.companyStdPlan = {};
          }

          $scope.calculatePremium(null);
        });

        $scope.save = function() {

          // Save std
          if (!$scope.enrollBenefits) {
            $scope.companyStdPlan.companyPlanId = null;
          }

          StdService.enrollStdPlanForUser(employeeId,
                                          $scope.selectedAmount,
                                          $scope.companyStdPlan,
                                          $scope.company.pay_period_definition,
                                          $scope.updateReason)
          .then(function() {
            var modalInstance = $scope.showSaveSuccessModal();
            modalInstance.result.then(function(){
                $scope.transitionToNextTab($scope.tabs);
            });
            $scope.myForm.$setPristine();
          }, function(error) {
            alert('Failed to save your benefits election. Please try again later.');
          })
        };

        $scope.openPlanDetailsModal = function() {
            $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_std_plan_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

    }]);

var ltdBenefitsSignup = employeeControllers.controller(
  'ltdBenefitsSignup',
  ['$scope',
   '$controller',
   '$modal',
   'LtdService',
    function ltdBenefitsSignup(
      $scope,
      $controller,
      $modal,
      LtdService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.enrollBenefits = true;

        $scope.hasPremium = function(premium) {
          var premiumNumber = parseFloat(premium);
          return _.isNumber(premiumNumber);
        };

        $scope.showSelectAmount = function() {

          return $scope.companyLtdPlan &&
            $scope.companyLtdPlan.allowUserSelectAmount &&
            $scope.enrollBenefits;
        };

        $scope.calculatePremium = function(amount) {

          LtdService.getEmployeePremiumForUserCompanyLtdPlan(
            $scope.employeeId, $scope.companyLtdPlan, amount)
          .then(function(premiumInfo) {
            $scope.companyLtdPlan.totalPremium = premiumInfo.totalPremium;
            $scope.companyLtdPlan.employeePremium = premiumInfo.employeePremiumPerPayPeriod;
            $scope.companyLtdPlan.effectiveBenefitAmount = premiumInfo.effectiveBenefitAmount;
          }, function(error){
            alert("Could not get premium info. Error is: " + error);
            $scope.companyLtdPlan.totalPremium = 0;
            $scope.companyLtdPlan.employeePremium = 0;
          });
        }

        $scope.companyPromise.then(function(company){
            $scope.company = company;
            LtdService.getLtdPlansForCompanyGroup($scope.userCompanyGroupId)
            .then(function(ltdPlans) {

                // For now, similar to basic life, simplify the problem space by
                // taking the first available plan for the company.
                if (ltdPlans.length > 0) {
                    $scope.companyLtdPlan = ltdPlans[0];
                    return $scope.companyLtdPlan;
                }
                return {};
            }).then(function(ltdPlan) {

              if (!$scope.companyLtdPlan) {
                $scope.companyLtdPlan = {};
              }

              $scope.calculatePremium(null);
            });

        })

        $scope.save = function() {
          // Save ltd
          if (!$scope.enrollBenefits) {
            $scope.companyLtdPlan.companyPlanId = null;
          }

          LtdService.enrollLtdPlanForUser(employeeId, $scope.selectedAmount,
            $scope.companyLtdPlan, $scope.company.pay_period_definition, $scope.updateReason)
          .then(function() {
              var modalInstance = $scope.showSaveSuccessModal();
              modalInstance.result.then(function(){
                $scope.transitionToNextTab($scope.tabs);
              });
              $scope.myForm.$setPristine();
            }
          , function(error) {
              alert('Failed to save your benefits election. Please try again later.');
            }
          );
        };

        $scope.openPlanDetailsModal = function() {
            $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_ltd_plan_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

    }]);

var hraBenefitsSignup = employeeControllers.controller(
  'hraBenefitsSignup',
  ['$scope',
   '$controller',
   '$modal',
   'HraService',
    function hraBenefitsSignup(
      $scope,
      $controller,
      $modal,
      HraService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.enrollBenefits = true;

        $scope.companyPromise.then(function(company){
          HraService.getPlansForCompanyGroup($scope.userCompanyGroupId).then(function(companyPlans) {
            if (companyPlans.length > 0) {
              $scope.companyPlan = companyPlans[0];
            }
            else
            {
              throw new Error('Did not locate active company HRA plans!');
            }
          });
        });

        $scope.companyPromise.then(function(company){
          HraService.getPersonPlanByUser(employeeId, company.id, true).then(function(personPlan) {
            $scope.personPlan = personPlan;
            // If HRA has been waived, uncheck the checkbox
            if (personPlan.personCompanyPlanId && !personPlan.companyPlanId) {
              $scope.enrollBenefits = false;
            }
          });
        });

        $scope.save = function() {
            // Save plan selection
            $scope.personPlan.companyPlanId = $scope.companyPlan.companyPlanId;
            var savePromise = HraService.savePersonPlan($scope.personPlan, $scope.updateReason, $scope.enrollBenefits);

            savePromise.then(
                function() {
                    var modalInstance = $scope.showSaveSuccessModal();
                    modalInstance.result.then(function(){
                        $scope.transitionToNextTab($scope.tabs);
                    });
                    $scope.myForm.$setPristine();
                }
              , function(error) {
                    alert('Failed to save your benefits election. Please try again later.');
                }
            );
        };

        $scope.openPlanDetailsModal = function() {
            $scope.detailsModalCompanyPlanToDisplay = $scope.companyPlan;
            $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_hra_plan_details.html',
              controller: 'planDetailsModalController',
              size: 'lg',
              scope: $scope
            });
        };

    }]);

var commonBenefitsSignup = employeeControllers.controller(
  'commonBenefitsSignup',
  ['$scope',
   '$controller',
    function commonBenefitsSignup(
      $scope,
      $controller){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        $scope.onSaveSuccess = function() {
            $scope.transitionToNextTab($scope.tabs);
        };

    }]);

var benefitSignupSummary = employeeControllers.controller(
  'benefitSignupSummary',
  ['$scope',
  '$state',
  '$controller',
  'BenefitSummaryService',
  function benefitSignupSummary(
    $scope,
    $state,
    $controller,
    BenefitSummaryService){

      $controller('employeeBenefitsSignup', {$scope: $scope});

       var employeeId = $scope.employeeId;
       $scope.companyPromise.then(function(company){
         BenefitSummaryService.getBenefitEnrollmentByUser(employeeId, company.id)
         .then(function(enrollments){
           $scope.enrollments = enrollments;
         }, function(error){
           alert('Failed to retreive your summary information. Please try again later.');
         });
       });

       $scope.goToState = function(state){
         $state.go(state);
         for (i = 0; i < $scope.$parent.tabs.length; i++) {
           $scope.$parent.tabs[i].active = ($scope.tabs[i].state === state);
         }
       };

       // Decide whether user has finished enrollment on a given benefit type
       $scope.completed = function(benefitType) {
         if (!$scope.enrollments || !$scope.enrollments[benefitType]) {
           return false;
         }

         return ($scope.enrollments[benefitType].status === 'SELECTED' ||
             $scope.enrollments[benefitType].status === 'WAIVED');
       };

       $scope.waived = function(benefitType) {
         if (!$scope.enrollments || !$scope.enrollments[benefitType]) {
           return false;
         }

         return $scope.enrollments[benefitType].status === 'WAIVED';
       };

       // Update panel class based on benefit enrollment status
       $scope.getPanelClass = function(benefitType) {
         if ($scope.completed(benefitType)) {
           return "panel-success";
         }

         return "panel-warning";
       };

       // Determine if the company provide a given benefit type
       $scope.companyProvide = function(benefitType) {
         if (!$scope.enrollments) {
           return false;
         }

         if ($scope.enrollments[benefitType]) {
           return true;
         }
         return false;
       };

       // Placeholder for document review flow
       // Set to return to employee dashboard for now
       $scope.continue = function() {
         $state.go('/employee');
       };
    }
  ]
);

var benefitsSignupControllerBase = employeeControllers.controller(
  'benefitsSignupControllerBase',
  ['$scope',
   '$state',
   '$stateParams',
   '$modal',
   'UserService',
    function benefitsSignupControllerBase(
      $scope,
      $state,
      $stateParams,
      $modal,
      UserService){

        $scope.employeeId = $stateParams.employee_id;

        // If no reason specified, bounce back to the summary page
        if (!$stateParams.updateReason) {
            alert('A reason for modifying benefit selection must be selected. Please try again from the "Modify Benefits" button.');
            $state.go('/employee');
        }

        $scope.updateReason = $stateParams.updateReason;

        $scope.companyPromise =  UserService.getCurUserInfo()
        .then(function(userInfo){
            $scope.company = userInfo.currentRole.company;
            $scope.userInfo = userInfo;
            $scope.userCompanyGroupId = null;
            if (userInfo.user.company_group_user && userInfo.user.company_group_user.length > 0){
              $scope.userCompanyGroupId = userInfo.user.company_group_user[0].company_group.id;
            }
            return userInfo.currentRole.company;
          });

        $scope.showSaveSuccessModal = function(){
          var modalInstance = $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_save_success.html',
              controller: 'benefitsSaveSuccessModalController',
              size: 'sm',
              backdrop: 'static',
              resolve: {
                  benefit_type: function () {
                    return $scope.benefit_type;
                  }
              }
          });
          return modalInstance;
        };

        $scope.transitionToNextTab = function(tabList){
            var sortedTabList = _.sortBy(tabList, 'id');

            var curTab = null;
            var curTabIndex = 0;
            var listSize = _.size(sortedTabList);
            for(var i=0; i<listSize; i++){
                curTab = sortedTabList[i];
                curTabIndex = i;
                if(curTab.active){
                    break;
                }
            }
            curTab.active = false;
            if(curTabIndex + 1 >= listSize){
                $state.go('/employee');
            }
            else{
                nextTab = sortedTabList[curTabIndex + 1];
                nextTab.active = true;
                $state.go(nextTab.state);
            }

        }

    }]);

var benefitsSaveSuccessModalController = employeeControllers.controller(
  'benefitsSaveSuccessModalController',
  ['$scope',
   '$state',
   '$modalInstance',
   'benefit_type',
    function benefitsSaveSuccessModalController(
      $scope,
      $state,
      $modalInstance,
      benefit_type){

        $scope.benefit_type = benefit_type;

        $scope.ok = function () {
          $modalInstance.close();
        };

    }]);

var employeeFamilyController = employeeControllers.controller(
  'employeeFamilyController',
  ['$scope',
   '$state',
   '$stateParams',
   '$modal',
   'PersonService',
  function employeeFamilyController(
    $scope,
    $state,
    $stateParams,
    $modal,
    PersonService){

    $('body').removeClass('onboarding-page');
    $scope.employeeId = $stateParams.employeeId;
  }
]);

var planDetailsModalController = employeeControllers.controller('planDetailsModalController',
  ['$scope',
   '$modal',
   '$modalInstance',
   function selectedBenefitsController(
    $scope,
    $modal,
    $modalInstance){
        $scope.closePlanDetailsModal = function() {
          $modalInstance.dismiss();
        };
}]);

var employeeHelpCenterController = employeeControllers.controller('employeeHelpCenterController',
  ['$scope',
  '$state',
  'UserService',
  'CompanyService',
  function($scope, $state, UserService, CompanyService) {
    UserService.getCurUserInfo().then(function(userInfo) {
      $scope.role = userInfo.currentRole.company_user_type.capitalize();
      $scope.company = userInfo.currentRole.company;
    });

    $scope.isAdmin = false;
    $scope.pageTitle = "Help Center";
    $scope.backToDashboard = function() {
      $state.go('/');
    };
  }
]);

var employeeViewTimeOffController = employeeControllers.controller('employeeViewTimeOffController',
  ['$scope',
   '$state',
   'UserService',
   function($scope, $state, UserService){
     $scope.role = 'Employee';
     $scope.isAdmin = false;

     UserService.getCurUserInfo().then(function(userInfo) {
        $scope.user = userInfo.user;
        $scope.user.role = userInfo.roles[0].company_user_type;
        $scope.company = userInfo.currentRole.company;
     });
   }
]);

var employeeViewWorkTimeSheetController = employeeControllers.controller('employeeViewWorkTimeSheetController',
  ['$scope',
   '$state',
   'UserService',
   function($scope, $state, UserService){
     UserService.getCurUserInfo().then(function(curUserInfo) {
       $scope.user = curUserInfo.user;
       $scope.role = curUserInfo.currentRole.company_user_type.capitalize();
       $scope.company = curUserInfo.currentRole.company;
     });
     $scope.isAdmin = false;
     $scope.pageTitle = 'Work Hour Timesheet';
     $scope.backToDashboard = function(){
       $state.go('/employee');
     };
   }
]);

var employeeManageTimePunchCardController = employeeControllers.controller('employeeManageTimePunchCardController',
  ['$scope',
   '$state',
   'UserService',
   function($scope, $state, UserService){
     UserService.getCurUserInfo().then(function(curUserInfo) {
       $scope.user = curUserInfo.user;
       $scope.role = curUserInfo.currentRole.company_user_type.capitalize();
       $scope.company = curUserInfo.currentRole.company;
     });
     $scope.isAdmin = false;
     $scope.pageTitle = 'Work Weekly Timesheet';
     $scope.backToDashboard = function(){
       $state.go('/employee');
     };
   }
]);

var directReportsViewController = employeeControllers.controller('directReportsViewController', [
    '$scope',
    '$state',
    'UserService',
    function($scope, $state, UserService){
      UserService.getCurUserInfo().then(function(curUserInfo){
        $scope.user = curUserInfo.user;
        $scope.role = curUserInfo.currentRole.company_user_type.capitalize();
        $scope.company = curUserInfo.currentRole.company;
      });

      $scope.backToDashboard = function(){
        $state.go('/employee');
      };
    }
]);



