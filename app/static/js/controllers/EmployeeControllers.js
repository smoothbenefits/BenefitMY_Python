var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
  ['$scope',
   '$location',
   '$state',
   '$stateParams',
   '$modal',
   'clientListRepository',
   'employeeBenefits',
   'UserService',
   'EmployeePreDashboardValidationService',
   'EmployeeLetterSignatureValidationService',
   'FsaService',
   'BasicLifeInsuranceService',
   'SupplementalLifeInsuranceService',
   'employeePayrollService',
   'EmploymentProfileService',
   'DirectDepositService',
   'StdService',
   'LtdService',
   'HraService',
   'DocumentService',
   'CompanyFeatureService',
  function ($scope,
            $location,
            $state,
            $stateParams,
            $modal,
            clientListRepository,
            employeeBenefits,
            UserService,
            EmployeePreDashboardValidationService,
            EmployeeLetterSignatureValidationService,
            FsaService,
            BasicLifeInsuranceService,
            SupplementalLifeInsuranceService,
            employeePayrollService,
            EmploymentProfileService,
            DirectDepositService,
            StdService,
            LtdService,
            HraService,
            DocumentService,
            CompanyFeatureService){
    $('body').removeClass('onboarding-page');
    var curUserId;
    var userPromise = UserService.getCurUserInfo();
    userPromise.then(function(response){
      $scope.employee_id = response.user.id;
      var employeeRole = _.findWhere(response.roles, {company_user_type:'employee'});
      if(employeeRole && employeeRole.new_employee){
        EmployeeLetterSignatureValidationService($scope.employee_id, 'Offer Letter', function(){
          EmployeePreDashboardValidationService.onboarding($scope.employee_id, function(){
            return response;
          }, function(redirectUrl){
            $location.path(redirectUrl);
          });
        },function(){
          $location.path('/employee/sign_letter/' + $scope.employee_id).search({letter_type:'Offer Letter'});
        });
      }
      else{
        EmployeePreDashboardValidationService.basicInfo($scope.employee_id, function(){
          return response;
        }, function(){
          //we need to redirect to edit profile page
          $location.path('/settings').search({forced:1});
        });
      }
      return response;
    });


    userPromise.then(function(userInfo){
      if(userInfo && userInfo.currentRole.company.id){
        employeeBenefits.enroll().get({userId:userInfo.user.id, companyId:userInfo.currentRole.company.id})
          .$promise.then(function(response){
                       $scope.benefits = response.benefits;
                       $scope.benefitCount = response.benefits.length;
          });
        employeeBenefits.waive().query({userId:userInfo.user.id, companyId:userInfo.currentRole.company.id})
          .$promise.then(function(waivedResponse){
            $scope.waivedBenefits = waivedResponse;
          });

        CompanyFeatureService.getDisabledCompanyFeatureByCompany(userInfo.currentRole.company.id)
        .then(function(features) {
          $scope.disabledFeatures = features;
        });
      }
    });

    userPromise.then(function(userInfo){
      if(userInfo) {
        DocumentService.getAllDocumentsForUser(userInfo.user.id).then(function(userDocs){
            $scope.documents = userDocs;
            $scope.documentCount = $scope.documents.length;
        });
      }
    });

     $scope.ViewDocument = function(documentId){
         $location.path('/employee/document/' + documentId);
     };

     $scope.goToState = function(state){
      $state.go(state);
     };

    userPromise.then(function(userInfo) {
      // FSA election data
      FsaService.getFsaElectionForUser(userInfo.user.id, userInfo.currentRole.company.id).then(function(fsaPlan){
        $scope.fsaElection = fsaPlan;
      });

      // Supplemental Life Insurance
      SupplementalLifeInsuranceService.getPlanByUser(userInfo.user.id, userInfo.currentRole.company.id).then(function(plan) {
        $scope.supplementalLifeInsurancePlan = plan;
      });

      // Basic Life Insurance
      BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(userInfo.user.id, userInfo.currentRole.company.id)
      .then(function(response){
        $scope.basicLifeInsurancePlan = response;
      });

      // W4 Form
      employeePayrollService.getEmployeeTaxSummaryByUserId(userInfo.user.id).then(function(response){
        $scope.w4Info = response;
      });

      // I9 Form
      EmploymentProfileService.getEmploymentAuthSummaryByUserId(userInfo.user.id).then(function(response){
        $scope.i9Info = response;
      });

      // Direct Deposit
      DirectDepositService.getDirectDepositByUserId(userInfo.user.id).then(function(response){
        $scope.directDepositAccounts = DirectDepositService.mapDtoToViewDirectDepositInBulk(response);
      });

      // STD
      StdService.getUserEnrolledStdPlanByUser(userInfo.user.id, userInfo.currentRole.company.id).then(function(response){
        $scope.userStdPlan = response;
      });

      // LTD
      LtdService.getUserEnrolledLtdPlanByUser(userInfo.user.id, userInfo.currentRole.company.id).then(function(response){
        $scope.userLtdPlan = response;
      });

      // HRA
      HraService.getPersonPlanByUser(userInfo.user.id, userInfo.currentRole.company.id).then(function(response){
        $scope.hraPlan = response;
      });

    });

    $scope.isLifeInsuranceWaived = function(employeeFamilyLifeInsurancePlan) {
        return (!employeeFamilyLifeInsurancePlan)
          || (!employeeFamilyLifeInsurancePlan.mainPlan)
          || (!employeeFamilyLifeInsurancePlan.mainPlan.id);
      };

    $scope.ViewDirectDeposit = function(editMode){
      $location.path('/employee/direct_deposit').search('edit', editMode);
    };
  }
]);

var viewDocument = employeeControllers.controller('viewDocument',
  ['$scope', '$location', '$stateParams', 'DocumentService', 'currentUser', 'documentRepository',
  function viewDocument($scope, $location, $stateParams, DocumentService, currentUser, documentRepository){
    $scope.document = {};
    var documentId = $stateParams.doc_id;
    var signatureUpdated = false;
    $scope.signatureCreatedDate = moment().format(DATE_FORMAT_STRING);
    var userPromise = currentUser.get().$promise
      .then(function(response){
        $scope.employee_id = response.user.id;
        return response.user.id;
      });

    var documentPromise = userPromise.then(function(userId){
      return DocumentService.getUserDocumentById(userId, documentId);
    });

    documentPromise.then(function(document){
      $scope.document = document;
      if(document.signature && document.signature.signature)
      {
        var signature = document.signature.signature;
        var separator = '<?xml';
        var sigComponents = signature.split(separator);
        $scope.signatureImage = sigComponents[0] + encodeURIComponent(separator + sigComponents[1]);
        $scope.signaturePresent = true;
        $scope.signatureCreatedDate = moment(document.signature.created_at).format(DATE_FORMAT_STRING);
      }
    });

    var $sigdiv = $("#doc_signature");
    if(_.isUndefined($sigdiv))
    {
      $scope.signaturePadError = 'Fatal error: Signature pad element cannot be found!';
    }
    $sigdiv.jSignature();
    $sigdiv.bind('change', function(e){
     signatureUpdated = true;
    });
    $scope.clearSignature = function(){
      $sigdiv.jSignature("reset");
      signatureUpdated = false;
    };
    $scope.signDocument = function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        var signaturePayload = "data:" + signatureData[0] + ',' + signatureData[1];
        documentRepository.sign.save({id:$scope.document.id}, {'signature':signaturePayload, 'signature_type': 'doc_sign'}, function(successResponse){
          $scope.signatureSaved = true;
          $scope.signatureImage = successResponse.signature.signature;
        }, function(failureResponse){
          $scope.signatureSaveFailed = true;
        });
      }
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
   'utilityServcie',
   function($scope,
            $state,
            $window,
            currentUser,
            employeePayrollService,
            utilityServcie){
    var userPromise = currentUser.get().$promise.then(function(response){
      return response.user.id;
    });

    userPromise.then(function(userId){
      employeePayrollService.getEmployeeTaxSummaryByUserId(userId)
      .then(function(response){
        $scope.employee = employeePayrollService.mapW4DtoToView(response);
        $scope.fields = utilityServcie.mapObjectToKeyPairArray('w4', response);
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

    var signatureUpdated = false;
    var $sigdiv = $("#auth_signature");
    if(_.isUndefined($sigdiv))
    {
      $scope.signaturePadError = 'Fatal error: Signature pad element cannot be found!';
    }
    $sigdiv.jSignature();
    $sigdiv.bind('change', function(e){
     signatureUpdated = true;
    });

    $scope.clearSignature = function(){
      $sigdiv.jSignature("reset");
      signatureUpdated = false;
    };

    $scope.openI9File = function(){
      if($scope.employee.downloadI9){
        var link = angular.element('#i9doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.signDocument = function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
        return;
      }
      if(!$scope.employee.downloadI9){
        alert('Please download the I-9 document and acknowledge you have read the entire form above.');
        return;
      }
      if($scope.employee.auth_type === 'Aaw' && !$scope.employee.expiration_na
         && !$scope.employee.auth_expiration) {
        alert('Please provide the expiration date for your work authorization document.');
        return;
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.signatureImage = "data:" + signatureData[0] + ',' + signatureData[1];
        EmploymentProfileService.saveEmploymentAuthByUserId($scope.employee, $scope.signatureImage).then(function(response){
          $state.go('employee_profile.i9');
        }, function(error){
          alert('Employment authorization has NOT been saved. Please try again later.');
        });
      }
    };

    $scope.editI9 = function(){
      $state.go('employee_profile.i9_edit');
    };
   }
  ]);

var directDeposit = employeeControllers.controller('employeeDirectDepositController',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   '$modal',
   'UserService',
   'DirectDepositService',
   function($scope,
            $state,
            $stateParams,
            $controller,
            $modal,
            UserService,
            DirectDepositService){

    // Inherit base modal controller for dialog window
    $controller('modalMessageControllerBase', {$scope: $scope});

    var userPromise = UserService.getCurUserInfo().then(function(response){
      $scope.person = response.user;
      $scope.person.role = 'Employee';
      return response.user.id;
    });

    userPromise.then(function(userId){
      DirectDepositService.getDirectDepositByUserId(userId).then(function(response){
        $scope.directDepositAccounts = DirectDepositService.mapDtoToViewDirectDepositInBulk(response);
      });
    });

    $scope.backToDashboard = function(){
      $state.go('/employee');
    };

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
        controller: 'directDepositModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          directDepositAccount: function () {
            return accountCopy;
          },
          userId: function() {
            return $scope.person.id;
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
  }]);

var directDepositModalController = employeeControllers.controller('directDepositModalController',
  ['$scope',
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

      $scope.resetAmountAndPercent = function(account){
        if(account.remainder_of_all){
          account.amount = 0;
          account.percentage = 0;
        }
        return account.remainder_of_all;
      };

      $scope.amountDisabled = function(account){
        return account.remainder_of_all || (account.percentage && account.percentage != 0);
      };

      $scope.percentageDisabled = function(account){
        return account.remainder_of_all || (account.amount && account.amount != 0);
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
  ]);

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
   '$stateParams',
   '$location',
   'PersonService',
   'currentUser',
   'EmployeePreDashboardValidationService',
  function($scope,
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
        $location.path('/employee/onboard/employment/' + $scope.employeeId);
      }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
}]);

var onboardEmployment = employeeControllers.controller('onboardEmployment',
  ['$scope', '$stateParams', '$location', '$window', 'employmentAuthRepository', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, $window, employmentAuthRepository, EmployeePreDashboardValidationService){
    $scope.employee = {
      auth_type: ''
    };
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
    var mapContract = function(viewObject, signature){
      var contract = {
        'worker_type': viewObject.auth_type,
        'uscis_number': viewObject.authNumber,
        'i_94': viewObject.I94Id,
        'passport': viewObject.passportId,
        'country': viewObject.passportCountry,
        'signature': {
          'signature': signature,
          'signature_type': 'work_auth'
        }
      };

      if (viewObject.auth_expiration){
        contract.expiration_date = moment(viewObject.auth_expiration).format('YYYY-MM-DD');
      }

      return contract;
    };

    var signatureUpdated = false;
    var $sigdiv = $("#auth_signature");
    if(_.isUndefined($sigdiv))
    {
      $scope.signaturePadError = 'Fatal error: Signature pad element cannot be found!';
    }
    $sigdiv.jSignature();
    $sigdiv.bind('change', function(e){
     signatureUpdated = true;
    });

    $scope.clearSignature = function(){
      $sigdiv.jSignature("reset");
      signatureUpdated = false;
    };

    $scope.acknowledgedI9=function(){
      $scope.employee.downloadI9 = !$scope.employee.downloadI9;
    };

    $scope.openI9File = function(){
      if($scope.employee.downloadI9){
        var link = angular.element('#i9doclink')[0];
        $window.open(link.href);
      }
    };

    $scope.signDocument = function(redirectUrl){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else if(!$scope.employee.downloadI9){
        alert('Please download the I-9 document and acknowledge you have read the entire form above.');
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.signatureImage = "data:" + signatureData[0] + ',' + signatureData[1];
        var contract = mapContract($scope.employee, $scope.signatureImage);
        employmentAuthRepository.save({userId: $scope.employeeId}, contract,
          function(){
            $location.path('/employee/onboard/tax/' + $scope.employeeId);
          }, function(){
            alert('Failed to add employment information');
          });
      }
    };
}]);

var onboardTax = employeeControllers.controller('onboardTax',
  ['$scope', '$stateParams', '$location', '$window', 'employeePayrollService', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, $window, employeePayrollService, EmployeePreDashboardValidationService){
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
        $location.path('/employee/onboard/complete/'+$scope.employeeId);
      });
    };
}]);

var onboardComplete = employeeControllers.controller('onboardComplete',
  ['$scope', '$stateParams', '$location', '$state', 'employeeSignature', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, $state, employeeSignature, EmployeePreDashboardValidationService){
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
    var signatureUpdated = false;
    var $sigdiv = $("#term_signature");
    if(_.isUndefined($sigdiv))
    {
      $scope.signaturePadError = 'Fatal error: Signature pad element cannot be found!';
    }
    $sigdiv.jSignature();
    $sigdiv.bind('change', function(e){
     signatureUpdated = true;
    });
    $scope.clearSignature = function(){
      $sigdiv.jSignature("reset");
      signatureUpdated = false;
    };
    $scope.submit=function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else{
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.termSignatureData = "data:" + signatureData[0] + ',' + signatureData[1];
        var contract = {
          'signature': $scope.termSignatureData,
          'signature_type': 'final'
        };
        employeeSignature.save({userId: $scope.employeeId}, contract,
          function(){
            $state.go('employee_family', {employeeId: $scope.employeeId, onboard:true});
          }, function(){
            alert('Failed to submit signature');
          });
      }
    }
}]);

var employeeAcceptDocument = employeeControllers.controller('employeeAcceptDocument',
  ['$scope', '$stateParams', '$location', 'documentRepository', 'EmployeeLetterSignatureValidationService',
  function($scope, $stateParams, $location, documentRepository, EmployeeLetterSignatureValidationService){
    $scope.employeeId = $stateParams.employee_id;
    var letterType = $location.search().letter_type;
    if(!letterType){
      letterType = 'Offer Letter';
    }

    var goToOnboarding = function(employeeId){
      $location.path('/employee/onboard/index/' + employeeId);
    };

    EmployeeLetterSignatureValidationService($scope.employeeId, letterType, function(){
      goToOnboarding($scope.employeeId);
    }, function(){
      $scope.displayAll = true;
    })
    documentRepository.byUser.query({userId:$scope.employeeId})
      .$promise.then(function(response){
        $scope.curLetter = _.find(response, function(letter){
          return letter.document_type.name === letterType;
        });
      });

    $('body').addClass('onboarding-page');
    var signatureUpdated = false;
    var $sigdiv = $('#letter_signature');
    if(_.isUndefined($sigdiv))
    {
      $scope.signaturePadError = 'Fatal error: Signature pad element cannot be found!';
    }
    $sigdiv.jSignature();
    $sigdiv.bind('change', function(e){
     signatureUpdated = true;
    });

    $scope.clearSignature = function(){
      $sigdiv.jSignature("reset");
      signatureUpdated = false;
    };

    $scope.submit = function(){

      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else{
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.letterSignatureData = "data:" + signatureData[0] + ',' + signatureData[1];
        var contract = {
          'signature': $scope.letterSignatureData,
          'signature_type': 'doc_sign'
        };
        documentRepository.sign.save({id:$scope.curLetter.id}, contract,
         function(){
           goToOnboarding($scope.employeeId);
         },
         function(err){
          alert('The signature has not been accepted. The reason is: ' + JSON.stringify(err.data));
         });
      }
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
      HraService){

      // Inherite scope from base
      $controller('benefitsSignupControllerBase', {$scope: $scope});

      var employeeId = $scope.employeeId;

      var basicLifePlans;
      var optionalLifePlans;
      var stdPlans;
      var ltdPlans;
      var fsaPlans;
      var hraPlans;

      var promise = $scope.companyIdPromise.then(function(companyId){
        return BasicLifeInsuranceService.getLifeInsurancePlansForCompanyByType(companyId, 'Basic');
      })
      .then(function(basicPlans) {
        basicLifePlans = basicPlans;
        return SupplementalLifeInsuranceService.getPlansForCompany(companyId);
      })
      .then(function(supplementalPlans) {
        supplementalLifePlans = supplementalPlans;
        return StdService.getStdPlansForCompany(companyId);
      })
      .then(function(stdPlansResponse) {
        stdPlans = stdPlansResponse;
        return LtdService.getLtdPlansForCompany(companyId);
      })
      .then(function(ltdPlansResponse) {
        ltdPlans = ltdPlansResponse;
        return FsaService.getFsaPlanForCompany(companyId);
      })
      .then(function(fsaPlansResponse) {
        fsaPlans = fsaPlansResponse;
        return HraService.getPlansForCompany(companyId);
      })
      .then(function(hraPlansResponse) {
        hraPlans = hraPlansResponse;
      });

      promise.then(function(result){

        $scope.tabs = [];
        $scope.tabs.push({
          "id": 1,
          "heading": "Health Benefits",
          "state":"employee_benefit_signup.health"
        });

        if (hraPlans.length > 0) {
          $scope.tabs.push({
            "id": 2,
            "heading": "HRA",
            "state": "employee_benefit_signup.hra"
          });
        }

        if(basicLifePlans.length > 0) {
          $scope.tabs.push({
            "id": 3,
            "heading": "Basic Life (AD&D)",
            "state":"employee_benefit_signup.basic_life"
          });
        }

        if (supplementalLifePlans.length > 0) {
          $scope.tabs.push({
            "id": 4,
            "heading": "Suppl. Life",
            "state":"employee_benefit_signup.supplemental_life"
          });
        }

        if (fsaPlans.length > 0) {
          $scope.tabs.push({
            "id": 5,
            "heading": "FSA",
            "state": "employee_benefit_signup.fsa"
          });
        }

        if (stdPlans.length > 0) {
          $scope.tabs.push({
            "id": 6,
            "heading": "STD",
            "state": "employee_benefit_signup.std"
          });
        }

        if (ltdPlans.length > 0) {
          $scope.tabs.push({
            "id": 7,
            "heading": "LTD",
            "state": "employee_benefit_signup.ltd"
          });
        }

        $scope.tabs.push({
          "id": 8,
          "heading": "Summary",
          "state": "employee_benefit_signup.summary"
        });

        // Always default to set the first tab be active.
        if ($scope.tabs.length > 0) {
          $scope.tabs[0].active = true;
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
      BasicLifeInsuranceService){

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
                return elem.relationship == 'self' || elem.relationship == 'spouse'});
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
                return elem.relationship == 'self' || elem.relationship == 'dependent'});
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

          $scope.companyIdPromise.then(function(companyId){
            benefitDisplayService(companyId, false, function(groupObj, nonMedicalArray, benefitCount){
              $scope.medicalBenefitGroup = groupObj;
              $scope.nonMedicalBenefitArray = nonMedicalArray;
            });

            //First get all the enrolled benefit list
            employeeBenefits.enroll().get({userId:employeeId, companyId:companyId})
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
                      return waived.company.id == companyId;
                    });


                    //Then get all the benefits associated with the company
                    benefitListRepository.get({clientId:companyId}).$promise.then(function(response){
                      _.each(response.benefits, function(availBenefit){
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
          var self = _.findWhere(selectedBenefitPlan.eligibleMemberCombo.familyList, {relationship: 'self'});
          self.selected = true;
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
          var saveRequest = {benefits:[],waived:[]};
          var invalidEnrollNumberList = [];
          var noPCPError = false;
          var hasEmptyRequiredPCP = false;
          $scope.companyIdPromise.then(function(companyId){

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

            saveRequest.waivedRequest = {company:companyId, waived:[]};
            _.each($scope.availablePlans, function(benefitPlan){
              if (benefitPlan.selected.benefit && benefitPlan.selected.benefit.benefit_plan.name === 'Waive'){
                if (benefitPlan.benefit_type === 'Medical' && !benefitPlan.selected.benefit.reason){
                  alert("Please select a reason to waive medical plan.");
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
            employeeBenefits.enroll().save({userId: employeeId, companyId: companyId}, saveRequest, function(){
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
   'benefitDisplayService',
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
      benefitDisplayService,
      FsaService,
      BasicLifeInsuranceService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        // FSA election data
        $scope.fsaUpdateReasons = [
          { text: '<Not making updates>', value: 0 },
          { text: 'New Enrollment or annual enrollment changes', value: 1 },
          { text: 'Dependent care cost provider changes', value: 2 },
          { text: 'Dependent satisfies or ceases to satisfy dependent eligibility requirements', value: 3 },
          { text: 'Birth/Death of spouse or dependent, adoption or placement for adoption', value: 4 },
          { text: 'Spouse\'s employment commenced/terminated', value: 5 },
          { text: 'Status change from full-time to part-time or vice versa by employee or spouse', value: 6 },
          { text: 'Eligibility or Ineligibility of Medicare/Medicaid', value: 7 },
          { text: 'Change from salaried to hourly or vice versa', value: 8 },
          { text: 'Marriage/Divorce/Legal Separation', value: 9 },
          { text: 'Unpaid leave of absence by employee or spouse', value: 10 },
          { text: 'Return from unpaid leave of absence by employee or spouse', value: 11 }
        ];

        $scope.companyIdPromise.then(function(companyId) {
          FsaService.getFsaPlanForCompany(companyId).then(function(fsaPlanForCompany) {
            // Current implementation implies one company will only have one FSA plan.
            // If use case changes in the future, we need to update the employee signup flow.
            $scope.fsaPlan = fsaPlanForCompany[0];
          });

          // Get current user selection
          FsaService.getFsaElectionForUser(employeeId, companyId).then(function(response) {
              $scope.fsaElection = response;
              if (response.update_reason && response.update_reason.length > 0){
                $scope.selectedFsaUpdateReason = _.findWhere($scope.fsaUpdateReasons, {text: response.update_reason});
              } else{
                $scope.selectedFsaUpdateReason = $scope.fsaUpdateReasons[0];
              }
            });
        });

        // Whether the user has selected a reason for updating
        // his/her FSA configuration.
        $scope.isFsaUpdateReasonSelected = function() {
          return $scope.selectedFsaUpdateReason && $scope.selectedFsaUpdateReason.value > 0;
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

        $scope.save = function(){
          // Save FSA selection if user specifies a reason
          if ($scope.isFsaUpdateReasonSelected()){
            $scope.fsaElection.update_reason = $scope.selectedFsaUpdateReason.text;
            $scope.fsaElection.company_fsa_plan = $scope.fsaPlan.companyPlanId;
          }

          // Set values to NULL if user chooses to waive FSA plan
          if ($scope.waivedFsa) {
            $scope.fsaElection.update_reason = '';
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
   'benefitDisplayService',
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
      benefitDisplayService,
      FsaService,
      BasicLifeInsuranceService){

        // Inherite scope from base
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.companyIdPromise.then(function(companyId){
          BasicLifeInsuranceService.getLifeInsurancePlansForCompanyByType(companyId, 'Basic').then(function(plans) {

            if (plans.length > 0) {
              $scope.basicLifeInsurancePlan = plans[0];
              $scope.basicLifeInsurancePlan.selected = true;
              // Ideally, basicLifeInsurancePlan should be user basic life insurance plan
              // plans returned here are company life insurance plan, which should be a property of
              // the basicLifeInsurancePlan rather than make the two parallel.
              $scope.basicLifeInsurancePlan.companyLifeInsurancePlan = plans[0];
            }

            // Get current user's basic life insurance plan situation
            BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employeeId, companyId).then(function(plan){
              $scope.basicLifeInsurancePlan.life_insurance_beneficiary = plan.life_insurance_beneficiary;
              $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary = plan.life_insurance_contingent_beneficiary;
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
          if (!$scope.basicLifeInsurancePlan.selected){
            BasicLifeInsuranceService.deleteBasicLifeInsurancePlanForUser(employeeId
              , function() {
                  var modalInstance = $scope.showSaveSuccessModal();
                  modalInstance.result.then(function(){
                      $scope.transitionToNextTab($scope.tabs);
                  });
                  $scope.myForm.$setPristine();
              }
              , function(error) {
                $scope.savedSuccess = false;
              });
          }
          else{
            BasicLifeInsuranceService.getInsurancePlanEnrollmentsByUser(employeeId, function(enrolledPlans){
              var enrolledBasic = _.find(enrolledPlans, function(plan){
                return plan.company_life_insurance.life_insurance_plan.insurance_type === 'Basic';
              });
              if (enrolledBasic){
                $scope.basicLifeInsurancePlan.enrolled = true;
                $scope.basicLifeInsurancePlan.id = enrolledBasic.id;
                $scope.basicLifeInsurancePlan.companyLifeInsurancePlan = enrolledBasic.company_life_insurance;
              }
              else{
                $scope.basicLifeInsurancePlan.enrolled = false;
              }

              $scope.basicLifeInsurancePlan.currentUserId = employeeId;

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
            }, function(error) {
              $scope.savedSuccess = false;
            });
          }
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
    function supplementalLifeBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      $modal,
      SupplementalLifeInsuranceService,
      SupplementalLifeInsuranceConditionService,
      PersonService){

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
            else if (member.relationship === 'spouse')
            {
                $scope.familyInfo.spousePerson = member;
            }
            else{
              $scope.familyInfo.hasChild = true;
            }
          });
        });

        $scope.companyPlans = [ { text: '<Waive Supplemental Life Insurance>', value: null } ];

        $scope.companyIdPromise.then(function(companyId){
          SupplementalLifeInsuranceService.getPlansForCompany(companyId).then(function(plans) {

            // Populate available company plans
            _.each(plans, function(plan) {
              $scope.companyPlans.push({ text: plan.planName, value: plan });
            });

            // Get current user's plan situation
            SupplementalLifeInsuranceService.getPlanByUser(employeeId, companyId, true).then(function(plan) {
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
        }

        $scope.getChildRate = function() {
            if (!$scope.familyInfo.hasChild) {
                return null;
            }
            return $scope.selectedCompanyPlan.value.planRates.childRate.ratePer10000;
        }

        $scope.computeSelfPremium = function() {
            // Refresh the local cached copy of self rate info
            $scope.selfRateInfo = $scope.getSelfRateInfo();
            if (!$scope.selfRateInfo) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.selfElectedAmount
                    * (1.0 - $scope.selfRateInfo.benefitReductionPercentage / 100.0) / 10000 * $scope.selfRateInfo.rate;
            return premium.toFixed(2);
        }

        $scope.computeSpousePremium = function() {
            // Refresh the local cached copy of self rate info
            $scope.spouseRateInfo = $scope.getSpouseRateInfo();
            if (!$scope.spouseRateInfo) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.spouseElectedAmount
                   * (1.0 - $scope.spouseRateInfo.benefitReductionPercentage / 100.0) / 10000 * $scope.spouseRateInfo.rate;
            return premium.toFixed(2);
        }

        $scope.computeChildPremium = function() {
            var rate = $scope.getChildRate();
            if (!rate) {
                return 0;
            }
            var premium =
                $scope.supplementalLifeInsurancePlan.childElectedAmount / 10000 * rate;
            return premium.toFixed(2);
        }

        $scope.save = function(){
          // Save life insurance
          if ($scope.isWaiveBenefitSelected()) {
            // Waive selected. Delete all user plans for this user
            SupplementalLifeInsuranceService.deletePlansForUser(employeeId).then(
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
            $scope.supplementalLifeInsurancePlan.selfPremiumPerMonth = $scope.computeSelfPremium();
            $scope.supplementalLifeInsurancePlan.spousePremiumPerMonth = $scope.computeSpousePremium();
            $scope.supplementalLifeInsurancePlan.childPremiumPerMonth = $scope.computeChildPremium();

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
          }
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

        $scope.companyIdPromise.then(function(companyId){

            StdService.getStdPlansForCompany(companyId).then(function(stdPlans) {

                // For now, similar to basic life, simplify the problem space by
                // taking the first available plan for the company.
                if (stdPlans.length > 0) {
                    $scope.companyStdPlan = stdPlans[0];
                    return $scope.companyStdPlan;
                }
                return {};
            }).then(function(stdPlan) {

                if (stdPlan.employerContributionPercentage === "100.00") {
                    $scope.companyStdPlan.employeePremium = 0.0;
                    return;
                }

                StdService.getEmployeePremiumForUserCompanyStdPlan($scope.employeeId, stdPlan)
                .then(function(premium) {
                    $scope.companyStdPlan.employeePremium = premium;
                });
            });
        });

        $scope.save = function() {

            // Save std
            var savePromise = $scope.enrollBenefits ?
                StdService.enrollStdPlanForUser(employeeId, $scope.companyStdPlan, $scope.updateReason) :
                StdService.deleteStdPlansForUser(employeeId);

            savePromise.then(
                function() {
                    var modalInstance = $scope.showSaveSuccessModal();
                    modalInstance.result.then(function(){
                        $scope.transitionToNextTab($scope.tabs);
                    });
                    $scope.myForm.$setPristine();
                }, function(error) {
                    alert('Failed to save your benefits election. Please try again later.');
                }
            );
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

        $scope.companyIdPromise.then(function(companyId){

            LtdService.getLtdPlansForCompany(companyId).then(function(ltdPlans) {

                // For now, similar to basic life, simplify the problem space by
                // taking the first available plan for the company.
                if (ltdPlans.length > 0) {
                    $scope.companyLtdPlan = ltdPlans[0];
                    return $scope.companyLtdPlan;
                }
                return {};
            }).then(function(ltdPlan) {

                if (ltdPlan.employerContributionPercentage === "100.00") {
                    $scope.companyLtdPlan.employeePremium = 0.0;
                    return;
                }

                LtdService.getEmployeePremiumForUserCompanyLtdPlan($scope.employeeId, ltdPlan)
                .then(function(premium) {
                    $scope.companyLtdPlan.employeePremium = premium;
                });
            });

        })

        $scope.save = function() {
            // Save ltd
            var savePromise = $scope.enrollBenefits ?
                LtdService.enrollLtdPlanForUser(employeeId, $scope.companyLtdPlan, $scope.updateReason) :
                LtdService.deleteLtdPlansForUser(employeeId);

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

        $scope.companyIdPromise.then(function(companyId){
            HraService.getPlansForCompany(companyId).then(function(companyPlans) {
                if (companyPlans.length > 0) {
                    $scope.companyPlan = companyPlans[0];
                }
                else
                {
                    throw new Error('Did not locate active company HRA plans!');
                }
            });
        });

        $scope.companyIdPromise.then(function(companyId){
          HraService.getPersonPlanByUser(employeeId, companyId, true).then(function(personPlan) {
            $scope.personPlan = personPlan;
          });
        });

        $scope.save = function() {
            // Save plan selection
            $scope.personPlan.companyPlanId = $scope.companyPlan.companyPlanId;
            var savePromise = $scope.enrollBenefits ?
                HraService.savePersonPlan($scope.personPlan, $scope.updateReason) :
                HraService.deletePlansForUser(employeeId);

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
       $scope.companyIdPromise.then(function (companyId){
         BenefitSummaryService.getBenefitEnrollmentByUser(employeeId, companyId)
         .then(function(enrollments){
           $scope.enrollments = enrollments;
         }, function(error){
           alert('Failed to retreive your summary information. Please try again later.');
         });
       });

       $scope.goToState = function(state){
         $state.go(state);
         for (i = 0; i < $scope.tabs.length; i++) {
           $scope.tabs[i].active = ($scope.tabs[i].state === state);
         }
       };

       // Decide whether user has finished enrollment on a given benefit type
       $scope.completed = function(benefitType) {
         if (!$scope.enrollments) {
           return false;
         }

         return ($scope.enrollments[benefitType].status === 'SELECTED' ||
             $scope.enrollments[benefitType].status === 'WAIVED');
       };

       $scope.waived = function(benefitType) {
         if (!$scope.enrollments) {
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
   'clientListRepository',
    function benefitsSignupControllerBase(
      $scope,
      $state,
      $stateParams,
      $modal,
      clientListRepository){

        $scope.employeeId = $stateParams.employee_id;

        // If no reason specified, bounce back to the summary page
        if (!$stateParams.updateReason) {
            alert('A reason for modifying benefit selection must be selected. Please try again from the "Modify Benefits" button.');
            $state.go('/employee');
        }

        $scope.updateReason = $stateParams.updateReason;

        $scope.companyIdPromise =  clientListRepository.get({userId:$scope.employeeId})
          .$promise.then(function(response){
            var company_id;
            _.each(response.company_roles, function(role){
              if(role.company_user_type==='employee'){
                company_id = role.company.id;
                companyId = company_id;
              }
            })
            return company_id;
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
                $state.go(curTab.next);
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
    var selfPerson = null;
    $scope.employeeId = $stateParams.employeeId;
    $scope.family=[];
    PersonService.getFamilyInfo($scope.employeeId)
    .then(function(family){
      _.each(family, function(member){
        if(member.relationship === 'self'){
          selfPerson = member;
        }
        else{
          $scope.family.push(member);
        }
      });
    });

    var openEditModal = function(member){
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/family_management/edit_form.html',
        controller: 'employeeFamilyMemberEditModalController',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          person: function () {
            return member;
          },
          employeeId: function(){
            return $scope.employeeId;
          }
        }
      });
      return modalInstance;
    };

    $scope.viewDetails = function(member){
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/family_management/view_member.html',
        controller: 'employeeFamilyMemberViewModalController',
        size: 'lg',
        backdrop: 'true',
        resolve: {
          member: function () {
            return member;
          }
        }
      });
      modalInstance.result.then(function(){
        openEditModal(member);
      });
    };

    $scope.editMember = function(member){
      openEditModal(member);
    };

    $scope.addMember = function(){
      var newPerson = {person_type:'family'};
      newPerson.address = selfPerson.address;
      newPerson.phone = selfPerson.phone;
      var modalInstance = openEditModal(newPerson);
      modalInstance.result
      .then(function(successResponse){
        if(successResponse){
          $state.reload();
        }
      });
    };

    $scope.isOnboarding = $stateParams.onboard === 'true';
  }
]);

var employeeFamilyMemberEditModalController = employeeControllers.controller(
  'employeeFamilyMemberEditModalController',
  ['$scope',
   '$modalInstance',
   'PersonService',
   'person',
   'employeeId',
  function employeeFamilyMemberEditModalController(
    $scope,
    $modalInstance,
    PersonService,
    person,
    employeeId){
    $scope.person = person;
    $scope.cancel = function(){
      $modalInstance.dismiss();
    };
    $scope.save = function(){
      PersonService.savePersonInfo(employeeId, $scope.person)
      .then(function(successResponse){
        alert('Save success!');
        $modalInstance.close(successResponse);
      }, function(errorResponse){
          alert('Failed to save the user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
  }
]);

var employeeFamilyMemberViewModalController = employeeControllers.controller(
  'employeeFamilyMemberViewModalController',
  ['$scope',
   '$modalInstance',
   'member',
    function employeeFamilyMemberViewModalController(
      $scope,
      $modalInstance,
      member){

        $scope.member = member;

        $scope.ok = function () {
          $modalInstance.dismiss();
        };

        $scope.edit = function(){
          $modalInstance.close();
        };

    }]);

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
