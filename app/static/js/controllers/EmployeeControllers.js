var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
    ['$scope',
     '$location',
     '$state', 
     '$stateParams',
     'clientListRepository',
     'employeeBenefits',
     'currentUser',
     'userDocument',
     'EmployeePreDashboardValidationService',
     'EmployeeLetterSignatureValidationService',
     'FsaService',
     'LifeInsuranceService',
     'employeePayrollService', 
     'employeeProfileService',
  function ($scope,
            $location,
            $state,
            $stateParams,
            clientListRepository,
            employeeBenefits,
            currentUser,
            userDocument,
            EmployeePreDashboardValidationService,
            EmployeeLetterSignatureValidationService,
            FsaService,
            LifeInsuranceService,
            employeePayrollService,
            employeeProfileService){

    $('body').removeClass('onboarding-page');
    var curUserId;
    var userPromise = currentUser.get().$promise
      .then(function(response){
        $scope.employee_id = response.user.id;
        var employeeRole = _.findWhere(response.roles, {company_user_type:'employee'});
        if(employeeRole && employeeRole.new_employee){
          EmployeeLetterSignatureValidationService($scope.employee_id, 'Offer Letter', function(){
            EmployeePreDashboardValidationService.onboarding($scope.employee_id, function(){
              return $scope.employee_id;
            }, function(redirectUrl){
              $location.path(redirectUrl);
            });
          },function(){
            $location.path('/employee/sign_letter/' + $scope.employee_id).search({letter_type:'Offer Letter'});
          });
        }
        else{
          EmployeePreDashboardValidationService.basicInfo($scope.employee_id, function(){
            return $scope.employee_id;
          }, function(){
            //we need to redirect to edit profile page
            $location.path('/settings').search({forced:1});
          });
        }
        return $scope.employee_id;
      });

    var companyPromise = userPromise.then(function(userId){
      if(userId){
        curUserId = userId;
        return clientListRepository.get({userId:userId}).$promise;
      }
    });

    var benefitPromise = companyPromise.then(function(response){
      if(response){
        var curCompanyId;
          _.each(response.company_roles, function(role){
            if (role.company_user_type === 'employee'){
              curCompanyId = role.company.id;
            }
          });
          return curCompanyId;
      }
    });

    benefitPromise.then(function(companyId){
      if(companyId){
        employeeBenefits.enroll().get({userId:curUserId, companyId:companyId})
          .$promise.then(function(response){
                       $scope.benefits = response.benefits;
                       $scope.benefitCount = response.benefits.length;
          });
        employeeBenefits.waive().query({userId:curUserId, companyId:companyId})
          .$promise.then(function(waivedResponse){
            $scope.waivedBenefits = waivedResponse;
          });
      }
    });

    var curUserPromise = currentUser.get().$promise.then(function(userResponse){
      return userResponse.user.id;
    });

     var documentPromise = curUserPromise.then(function(userId){
                                               return userDocument.query({userId:userId}).$promise;
                         });

     documentPromise.then(function(response){
                          $scope.documents = response;
                          $scope.documentCount = response.length;
                          });

     $scope.ViewDocument = function(documentId){
         $location.path('/employee/document/' + documentId);
     };

     $scope.goToState = function(state){
      $state.go(state);
     };
    
    curUserPromise.then(function(userId) {
      // FSA election data
      FsaService.getFsaElectionForUser(userId, function(response) {
        $scope.fsaElection = response;
      });

      // Life Insurance
      LifeInsuranceService.getInsurancePlanEnrollmentsForAllFamilyMembersByUser(userId, function(response) {
        $scope.familyInsurancePlan = response;
      });

      LifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(userId, function(response){
        $scope.basicLifeInsurancePlan = response;
      });

      // W4 Form
      employeePayrollService.getEmployeeTaxSummaryByUserId(userId).then(function(response){
        $scope.w4Info = response;
      });

      // I9 Form
      employeeProfileService.getEmploymentAuthSummaryByUserId(userId).then(function(response){
        $scope.i9Info = response;
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

var addFamily = employeeControllers.controller('addFamily', 
 ['$scope', 
  '$location', 
  '$stateParams', 
  'personInfoService',
  function addFamily(
    $scope, 
    $location, 
    $stateParams, 
    personInfoService){

  var employeeId = $stateParams.employee_id;
  $scope.employeeId = employeeId;
  $scope.person = {person_type:'family'};
  personInfoService.getPersonInfo(employeeId, function(retrievedInfo){
    if(retrievedInfo){
      $scope.person.address = retrievedInfo.address;
      $scope.person.phone = retrievedInfo.phone;
    }
  });


  $scope.addMember = function(){
    personInfoService.savePersonInfo(employeeId, $scope.person, function(successResponse){
      $location.path('/employee/benefits/' + employeeId);
    }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
    });
  }
}]);

var viewDocument = employeeControllers.controller('viewDocument',
  ['$scope', '$location', '$stateParams', 'userDocument', 'currentUser', 'documentRepository',
  function viewDocument($scope, $location, $stateParams, userDocument, currentUser, documentRepository){
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
      var document = userDocument.query({userId:userId}).$promise
        .then(function(response){
          return _.find(response, function(d)
          {
            return d.id.toString() === documentId;
          });
        });
      return document;
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
   '$location', 
   'tabLayoutGlobalConfig',
   function($scope, 
            $state,
            $location, 
            tabLayoutGlobalConfig){
    $scope.section = _.findWhere(tabLayoutGlobalConfig, {section_name: 'employee_payroll'});

    $scope.goToState = function(state){
      $state.go(state);
    };

    $scope.backToDashboard = function(){
      $location.path('/employee');
    };
   }
  ]);

var employeeW4Controller = employeeControllers.controller('employeeW4Controller', 
  ['$scope',
   '$state',
   'currentUser', 
   'employeePayrollService', 
   function($scope, 
            $state, 
            currentUser, 
            employeePayrollService){
    var userPromise = currentUser.get().$promise.then(function(response){
      return response.user.id;
    });

    userPromise.then(function(userId){
      employeePayrollService.getEmployeeTaxByUserId(userId).then(function(taxFields){
        $scope.fields = taxFields;
      });
    });

    $scope.calculateTotal = function(){
      var total = employeePayrollService.getMarriageNumberForUser($scope.employee.withholdingType);
      total += $scope.employee.dependent_count;
      if($scope.employee.childExpense && total){
        total += parseInt($scope.employee.childExpense);
      }
      if($scope.employee.headOfHousehold && total){
        total += parseInt($scope.employee.headOfHousehold);
      }
      if(!total)
      {
        total = undefined;
      }
      $scope.employee.calculated_points = total;
      if(!$scope.employee.user_defined_set){
        $scope.employee.user_defined_points = $scope.employee.calculated_points;
      }
    };

    $scope.userDefinedPointsSet = function(){
      $scope.employee.user_defined_set = true;
    };

    $scope.acknowledgeW4 = function(){
      $scope.employee.downloadW4 = !$scope.employee.downloadW4;
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
        alert('Please enter the extra amount of your paycheck to withhold (Line 6 on your W-4)');
        return;
      }

      // Add marriage number to $scope object
      $scope.employee.marriage = employeePayrollService.getMarriageNumberForUser($scope.employee.withholdingType);
      userPromise.then(function(userId){
        employeePayrollService.saveEmployeeTaxByUserId(userId, $scope.employee).then(function(response){
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
   '$location',
   'tabLayoutGlobalConfig', 
   function ($scope, 
             $state, 
             $location, 
             tabLayoutGlobalConfig){
    $scope.section = _.findWhere(tabLayoutGlobalConfig, { section_name: 'employee_profile'});

    $scope.goToState = function(state){
      $state.go(state);
    };

    $scope.backToDashboard = function(){
      $location.path('/employee');
    };
   }
  ]);

var employeeI9Controller = employeeControllers.controller('employeeI9Controller', 
  ['$scope',
   '$state',
   'currentUser', 
   'employeeProfileService', 
   function($scope,
            $state,
            currentUser,
            employeeProfileService){
    $scope.employee = {auth_type: ''};

    var userPromise = currentUser.get().$promise.then(function(response){
      return response.user.id;
    });

    userPromise.then(function(userId){
      // assign user id to current employee
      $scope.employee.userId = userId;

      employeeProfileService.getEmploymentAuthByUserId(userId).then(function(response){
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

    $scope.acknowledgedI9 = function(){
      $scope.employee.downloadI9 = !$scope.employee.downloadI9;
    };

    $scope.signDocument = function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      if(!$scope.employee.downloadI9){
        alert('Please download the I-9 document and acknowledge you have read the entire form above.');
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.signatureImage = "data:" + signatureData[0] + ',' + signatureData[1];
        employeeProfileService.saveEmploymentAuthByUserId($scope.employee, $scope.signatureImage).then(function(response){
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

var employeeInfo = employeeControllers.controller('employeeInfoController',
  ['$scope', '$location', '$stateParams', 'profileSettings', 'currentUser', 'employmentAuthRepository', 'employeeTaxRepository',
  function($scope, $location, $stateParams, profileSettings, currentUser, employmentAuthRepository, employeeTaxRepository){
    var infoObject = _.findWhere(profileSettings, { name: $stateParams.type });
    $scope.info = { type: $stateParams.type, type_display: infoObject.display_name };
    $scope.person = { role: 'Employee' };

    if ($stateParams.type === 'i9'){
      $scope.isUpdateW4 = false;
      $scope.isUpdateI9 = true;
    }

    if ($stateParams.type === 'w4'){
      $scope.isUpdateW4 = true;
      $scope.isUpdateI9 = false;
    }

    var userPromise = currentUser.get().$promise.then(function(response){
      $scope.person.first_name = response.user.first_name;
      $scope.person.last_name = response.user.last_name;
      return response.user.id;
    });

    userPromise.then(function(userId){
      if ($scope.info.type === 'i9'){
        employmentAuthRepository.get({userId: userId}).$promise.then(function(response){
          $scope.info.fields = convertResponse(response, $scope.info.type);
        });
      } else if ($scope.info.type === 'w4'){
        employeeTaxRepository.get({userId: userId}).$promise.then(function(response){
          $scope.info.fields = convertResponse(response, $scope.info.type);
        });
      }

    });

    var convertResponse = function(res, type){
      var pairs = _.pairs(res);
      var validFields = _.findWhere(profileSettings, {name: type}).valid_fields;
      var output = [];
      _.each(pairs, function(pair){
        var key = pair[0];
        var inSetting = _.findWhere(validFields, {name: key});
        if (inSetting){
          if (inSetting.datamap){
            var value = pair[1];
            var mappedValue = _.find(inSetting.datamap, function(map){
              return map[0] === value.toString();
            });
            if (!mappedValue){
              inSetting.value = 'UNKNOWN';
            } else{
              inSetting.value = mappedValue[1];
            }
          } else{
            inSetting.value = pair[1];
          }
          output.push(inSetting);
        }
      });

      return output;
    }

    $scope.backToDashboard = function(){
      $location.path('/employee');
    };

    $scope.editW4 = function(){
      $location.path('/employee/info/edit').search('type', 'w4');
    };

    $scope.editI9 = function(){
      $location.path('/employee/info/edit').search('type', 'i9');
    };
  }]);

var directDeposit = employeeControllers.controller('employeeDirectDepositController',
  ['$scope',
   '$state', 
   '$stateParams',
   '$location',
   'currentUser',
   'DirectDepositService',
   function($scope,
            $state,  
            $stateParams,
            $location,
            currentUser,
            DirectDepositService){
    var existingDirectDepositAccountIds = [];
    $scope.editMode = $stateParams.edit;
    $scope.directDepositAccounts = [];
    $scope.bankAccountTypes = ['Checking', 'Saving'];

    $scope.backToDashboard = function(){
      $location.path('/employee');
    };

    $scope.removeBankAccount = function(account){
      var index = $scope.newDirectDepositAccounts.indexOf(account);
      $scope.newDirectDepositAccounts.splice(index, 1);
    };

    $scope.editDirectDeposit = function(account){
      account.inEditMode = true;
    };

    $scope.exitEditMode = function(account){
      account.inEditMode = false;
    };

    $scope.viewExistingDirectDepositAccounts = function(){
      $scope.addingNewAccount = false;
      $scope.newDirectDepositAccounts = [];
    };

    $scope.addBankAccount = function(){
      $scope.newDirectDepositAccounts.push({ account_type: $scope.bankAccountTypes[0]});
    };

    $scope.addNewDirectDepositAccount = function(){
      $scope.addingNewAccount = true;
      $scope.newDirectDepositAccounts = [];
      $scope.newDirectDepositAccounts.push({account_type: $scope.bankAccountTypes[0]});
    };

    $scope.deleteDirectDeposit = function(account){

      var confirmed = confirm('About to delete a direct deposit account. Are you sure?');
      if (confirmed === true){
        var directDeposit = DirectDepositService.mapViewDirectDepositToDto(account);
        DirectDepositService.deleteDirectDepositById(directDeposit, function(response){
          getDirectDeposit(account.user);
        }, function(error){
          alert('Failed to delete direct deposit account. Please try again later.');
        });
      }
    };

    $scope.updateDirectDeposit = function(account){
      var directDeposit = DirectDepositService.mapViewDirectDepositToDto(account);
      DirectDepositService.updateDirectDepositByUserId(directDeposit, function(response){
        $state.transitionTo($state.current, $stateParams, {
            reload: true,
            inherit: false,
            notify: true
        });
      }, function(error){
        alert('Failed to update direct deposit account. Please try again later.');
      });
    };

    var userPromise = currentUser.get().$promise.then(function(response){
      $scope.person = response.user;
      $scope.person.role = 'Employee';
      return response.user.id;
    });

    var getDirectDeposit = function(userId){
      DirectDepositService.getDirectDepositByUserId(userId, function(response){
        $scope.directDepositAccounts = DirectDepositService.mapDtoToViewDirectDeposit(response);
        if (response.length === 0){
          $scope.hasDirectDeposit = false;
          $scope.directDepositAccounts.push({ account_type: $scope.bankAccountTypes[0], inEditMode: false });
        }
        else {
          $scope.hasDirectDeposit = true;
          existingDirectDepositAccountIds = _.map($scope.directDepositAccounts, function(account){
            return account.id;
          });

          _.each($scope.directDepositAccounts, function(account){
            account.inEditMode = false;
          });
        }
      });
    };

    $scope.resetAmountAndPercent = function(account){
      if(account.remainder_of_all){
        account.amount = 0;
        account.percentage = 0;
      }
      return account.remainder_of_all;
    };

    userPromise.then(function(userId){
      getDirectDeposit(userId);
    });

    $scope.submitDirectDeposit = function(){
      var directDepositDtos = [];
      // Map direct deposit domain model to DTO, one by one
      _.each($scope.newDirectDepositAccounts, function(account){
        account.user = $scope.person.id;
        var dto = DirectDepositService.mapViewDirectDepositToDto(account);
        directDepositDtos.push(dto);
      });

      DirectDepositService.createDirectDepositByUserId($scope.person.id, directDepositDtos, function(response){
        $state.transitionTo($state.current, $stateParams, {
            reload: true,
            inherit: false,
            notify: true
        });
      }, function(error){
        alert('Failed to create direct deposit record due to ' + error);
      });
    };
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
  ['$scope', '$stateParams', '$location', 'personInfoService', 'currentUser', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, personInfoService, currentUser, EmployeePreDashboardValidationService){

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

    $scope.addBasicInfo = function(){
      var birthDate = $scope.employee.birth_date;
      $scope.employee.birth_date = moment(birthDate).format('YYYY-MM-DD');
      personInfoService.savePersonInfo($scope.employeeId, $scope.employee, function(successResponse){
        $location.path('/employee/onboard/employment/' + $scope.employeeId);
      }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
}]);

var onboardEmployment = employeeControllers.controller('onboardEmployment',
  ['$scope', '$stateParams', '$location', 'employmentAuthRepository', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, employmentAuthRepository, EmployeePreDashboardValidationService){
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
  ['$scope', '$stateParams', '$location','employeeTaxRepository', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, employeeTaxRepository, EmployeePreDashboardValidationService){
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

    var getMarriageNumber = function(){
      if($scope.employee.withholdingType ==='married'){
        return 2;
      }
      else{
        return 1;
      }
    };

    $scope.calculateTotal = function(){
      var total = getMarriageNumber();
      total += $scope.employee.dependent_count;
      if($scope.employee.childExpense && total){
        total += parseInt($scope.employee.childExpense);
      }
      if($scope.employee.headOfHousehold && total){
        total += parseInt($scope.employee.headOfHousehold);
      }
      if(!total)
      {
        total = undefined;
      }
      $scope.employee.calculated_points = total;
      if(!$scope.employee.user_defined_set){
        $scope.employee.user_defined_points = $scope.employee.calculated_points;
      }
    };

    $scope.userDefinedPointsSet = function(){
      $scope.employee.user_defined_set = true;
    };

    $scope.acknowledgeW4 = function(){
      $scope.employee.downloadW4 = !$scope.employee.downloadW4;
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
        alert('Please enter the extra amount of your paycheck to withhold (Line 6 on your W-4)');
        return;
      }
      var empAuth = {
        marriage: getMarriageNumber(),
        dependencies: $scope.employee.dependent_count,
        head: $scope.employee.headOfHousehold,
        tax_credit: $scope.employee.childExpense,
        calculated_points: $scope.employee.calculated_points,
        user_defined_points: $scope.employee.user_defined_points,
        extra_amount: $scope.employee.extra_amount
      };
      employeeTaxRepository.save({userId:$scope.employeeId}, empAuth,
        function(response){
          $location.path('/employee/onboard/complete/'+$scope.employeeId);
        });
    };
}]);

var onboardComplete = employeeControllers.controller('onboardComplete',
  ['$scope', '$stateParams', '$location', 'employeeSignature', 'EmployeePreDashboardValidationService',
  function($scope, $stateParams, $location, employeeSignature, EmployeePreDashboardValidationService){
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
            $location.path('/employee');
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
   'LifeInsuranceService',
    function employeeBenefitsSignup(
      $scope,
      $state,
      $stateParams,
      $controller,
      LifeInsuranceService){

      // Inherite scope from base 
      $controller('benefitsSignupControllerBase', {$scope: $scope});

      var employeeId = $scope.employeeId;

      var basicLifePlans;
      var optionalLifePlans;

      var promise = $scope.companyIdPromise.then(function(companyId){
        return LifeInsuranceService.getLifeInsurancePlansForCompanyByType(companyId, 'Basic');
      })
      .then(function(basicPlans) {
        basicLifePlans = basicPlans;
        return LifeInsuranceService.getLifeInsurancePlansForCompanyByType(companyId, 'Extended');
      })
      .then(function(optionalPlans) {
        optionalLifePlans = optionalPlans;
      })

      promise.then(function(result){
        
        $scope.tabs = [];
        $scope.tabs.push({
              "heading": "Health Benefits",
              "state":"employee_benefit_signup.health"
        });

        if(basicLifePlans.length > 0) {
          $scope.tabs.push({
              "heading": "Basic Life",
              "state":"employee_benefit_signup.basic_life"
          });
        }

        if ($scope.supplementalLifeInsuranceEnabled) {
          if (optionalLifePlans.length > 0) {
            $scope.tabs.push({
                  "heading": "Optional Life",
                  "state":"employee_benefit_signup.optional_life"
              });
          }
        }

        $scope.tabs.push({
              "heading": "FSA",
              "state":"employee_benefit_signup.fsa"
          });

        // Always default to set the first tab be active.
        if ($scope.tabs.length > 0) {
          $scope.tabs[0].active = true;
        }

      });

      $scope.go_to_state = function(state) {
        $state.go(state);
      };

      $scope.addMember = function(){
        $state.go('/employee/add_family/:employee_id', { employee_id:employeeId });
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
   'employeeFamily',
   'benefitDisplayService',
   'FsaService',
   'LifeInsuranceService',
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
      employeeFamily,
      benefitDisplayService,
      FsaService,
      LifeInsuranceService){

        // Inherite scope from base 
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var medicalPlans = [];
        var dentalPlans = [];
        var visionPlans = [];
        var employeeId = $scope.employeeId;
        var companyId;
        $scope.employee_id = employeeId;
        $scope.availablePlans = [];
        $scope.family = [];
        $scope.selectedBenefits =[];
        $scope.selectedBenefitHashmap = {};

        employeeFamily.get({userId:employeeId}).$promise.then(function(response){
          _.each(response.family, function(member){
            member.ticked = false;
            $scope.family.push(member);
          });
        });

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
          _.each($scope.availablePlans, function(benefitTypePlan){
            var enrolledList = [];
            if (typeof benefitTypePlan.selected.eligibleMemberCombo != 'undefined'){
              _.each(benefitTypePlan.selected.eligibleMemberCombo.familyList, function(member){
                if(member.selected)
                {
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
          saveRequest.waivedRequest = {company:companyId, waived:[]};
          _.each($scope.availablePlans, function(benefitPlan){
              if (benefitPlan.selected.benefit && benefitPlan.selected.benefit.benefit_plan.name === 'Waive'){
                if (benefitPlan.benefit_type === 'Medical' && !benefitPlan.selected.benefit.reason){
                  alert("Please select a reason to waive medical plan.");
                  $location.path('/employee/benefits/' + $scope.employee_id);
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

          employeeBenefits.waive().save({userId: employeeId}, saveRequest.waivedRequest, function(){}, 
             function(errorResponse){
              alert('Saving waived selection failed because: ' + errorResponse.data);
              $scope.savedSuccess = false;
            });
        

          employeeBenefits.enroll().save({userId: employeeId, companyId: companyId}, saveRequest, function(){
              $scope.showSaveSuccessModal();
              $scope.myForm.$setPristine();
            }, function(){
              $scope.savedSuccess = false;
            });
        };

        $scope.benefit_type = 'Health Benefits';

        $scope.openPlanDetailsModal = function() {
            $scope.planDetailsModalInstance = $modal.open({
              templateUrl: '/static/partials/benefit_selection/modal_health_plan.html',
              controller: 'healthBenefitsSignup',
              size: 'lg',
              scope: $scope
            });
        };

        $scope.closePlanDetailsModal = function() {
          if ($scope.planDetailsModalInstance) {
            $scope.planDetailsModalInstance.dismiss();
            $scope.planDetailsModalInstance = null;
          }
        };
    }]);

var fsaBenefitsSignup = employeeControllers.controller(
  'fsaBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'employeeFamily',
   'benefitDisplayService',
   'FsaService',
   'LifeInsuranceService',
    function fsaBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      employeeFamily,
      benefitDisplayService,
      FsaService,
      LifeInsuranceService){

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
        $scope.selectedFsaUpdateReason = $scope.fsaUpdateReasons[0];
        FsaService.getFsaElectionForUser(employeeId, function(response) {
          $scope.fsaElection = response;
        });

        // Whether the user has selected a reason for updating 
        // his/her FSA configuration.
        $scope.isFsaUpdateReasonSelected = function() {
          return $scope.selectedFsaUpdateReason.value > 0;
        };

        $scope.save = function(){
          // Save FSA selection if user specifies a reason
          if ($scope.isFsaUpdateReasonSelected()){
            $scope.fsaElection.update_reason = $scope.selectedFsaUpdateReason.text;
            FsaService.saveFsaElection($scope.fsaElection
              , function() {
                $scope.showSaveSuccessModal();
                $scope.myForm.$setPristine();
              }
              , function() {
                $scope.savedSuccess = false;
              });
          }
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
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'employeeFamily',
   'benefitDisplayService',
   'FsaService',
   'LifeInsuranceService',
    function basicLifeBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      employeeFamily,
      benefitDisplayService,
      FsaService,
      LifeInsuranceService){
        
        // Inherite scope from base 
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.companyIdPromise.then(function(companyId){
          LifeInsuranceService.getLifeInsurancePlansForCompany(companyId, function(plans) {

            // Populate available company plans
            _.each(plans, function(plan) {
              // separate basic life insurance from supplemental life insurance.
              // for now, it will pick the last basic life insurance defined by broker.
              if (plan.life_insurance_plan.insurance_type === 'Basic'){
                $scope.basicLifeInsurancePlan = plan;
                $scope.basicLifeInsurancePlan.selected = true;
              }
            });

            // Get current user's basic life insurance plan situation
            LifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employeeId, function(plan){
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

        $scope.save = function(){

          ///////////////////////////////////////////////////////////////////////////
          // Save basic life insurance
          // TO-DO: Need to better organize the logic to save basic life insurance
          ///////////////////////////////////////////////////////////////////////////
          if (!$scope.basicLifeInsurancePlan.selected){
            LifeInsuranceService.deleteBasicLifeInsurancePlanForUser(employeeId
              , function() {
                $scope.showSaveSuccessModal();
                $scope.myForm.$setPristine();
              }
              , function(error) {
                $scope.savedSuccess = false;
              });
          }
          else{
            LifeInsuranceService.getInsurancePlanEnrollmentsByUser(employeeId, function(enrolledPlans){
              var enrolledBasic = _.find(enrolledPlans, function(plan){ 
                return plan.company_life_insurance.life_insurance_plan.insurance_type === 'Basic';
              });
              if (enrolledBasic){
                $scope.basicLifeInsurancePlan.enrolled = true;
                $scope.basicLifeInsurancePlan.id = enrolledBasic.id;
              }
              else{
                $scope.basicLifeInsurancePlan.enrolled = false;
              }
              
              $scope.basicLifeInsurancePlan.currentUserId = employeeId;

              LifeInsuranceService.saveBasicLifeInsurancePlanForUser($scope.basicLifeInsurancePlan
              , function() {
                $scope.showSaveSuccessModal();
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

var optionalLifeBenefitsSignup = employeeControllers.controller(
  'optionalLifeBenefitsSignup',
  ['$scope',
   '$state',
   '$location',
   '$stateParams',
   '$controller',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'employeeFamily',
   'benefitDisplayService',
   'FsaService',
   'LifeInsuranceService',
    function optionalLifeBenefitsSignup(
      $scope,
      $state,
      $location,
      $stateParams,
      $controller,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      employeeFamily,
      benefitDisplayService,
      FsaService,
      LifeInsuranceService){
        
        // Inherite scope from base 
        $controller('benefitsSignupControllerBase', {$scope: $scope});

        var employeeId = $scope.employeeId;

        $scope.lifeInsurancePlans = [ { text: '<Waive Life Insurance>', value: '0' } ];
        $scope.selectedLifeInsurancePlan = $scope.lifeInsurancePlans[0];

        $scope.companyIdPromise.then(function(companyId){
          LifeInsuranceService.getLifeInsurancePlansForCompany(companyId, function(plans) {

            // Populate available company plans
            _.each(plans, function(plan) {
              $scope.lifeInsurancePlans.push({ text: plan.life_insurance_plan.name, value: plan.id });  
            });

            // Get current user's family life insurance plan situation
            LifeInsuranceService.getInsurancePlanEnrollmentsForAllFamilyMembersByUser(employeeId, function(familyPlan) {
              $scope.familyLifeInsurancePlan = familyPlan;

              // Determine the right plan option to select
              if (!$scope.isLifeInsuranceWaived($scope.familyLifeInsurancePlan)) {
                var optionToSelect = _.where($scope.lifeInsurancePlans, {value:$scope.familyLifeInsurancePlan.mainPlan.life_insurance.life_insurance_plan.id});
                if (optionToSelect.length > 0) {
                  $scope.selectedLifeInsurancePlan = optionToSelect[0];
                }
              }
            });
          });
        });

        // User should be able to add up to 4 beneficiaries of life insurance
        $scope.addBeneficiary = function(){
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.push({});
        };

        $scope.addContingentBeneficiary = function(){
          if (!$scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary){
            $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary = [];
          }
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.push({});
        };

        $scope.removeBeneficiary = function(beneficiary){
          var index = $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.indexOf(beneficiary);
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.splice(index, 1);
        };

        $scope.removeContingentBeneficiary = function(beneficiary){
          var index = $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.indexOf(beneficiary);
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.splice(index, 1);
        };

        // Whether the user selected to waive life insurance
        $scope.isWaiveLifeInsuranceSelected = function() {
          return $scope.selectedLifeInsurancePlan.value === "0";
        };

        // Whether the current status of the given employee's family life insurance
        // plan indicates a waived/not-yet-enrolled state
        $scope.isLifeInsuranceWaived = function(employeeFamilyLifeInsurancePlan) {
          return (!employeeFamilyLifeInsurancePlan) 
            || (!employeeFamilyLifeInsurancePlan.mainPlan)
            || (!employeeFamilyLifeInsurancePlan.mainPlan.id);
        };

        $scope.save = function(){
          // Save life insurance
          if ($scope.isWaiveLifeInsuranceSelected()) {
            // Waive selected. Delete all user plans for this user
            LifeInsuranceService.deleteFamilyLifeInsurancePlanForUser(employeeId
              , function() {
                $scope.showSaveSuccessModal();
                $scope.myForm.$setPristine();
              }
              , function(error) {
                $scope.savedSuccess = false;
            });
          } else {
            $scope.familyLifeInsurancePlan.selectedCompanyPlan = $scope.selectedLifeInsurancePlan.value;
            LifeInsuranceService.saveFamilyLifeInsurancePlanForUser($scope.familyLifeInsurancePlan
              , function() {
                $scope.showSaveSuccessModal();
                $scope.myForm.$setPristine();
              }
              , function(error) {
                $scope.savedSuccess = false;
                alert('Failed to save your beneficiary information. Please make sure all required fields have been filled.');
              });
          }
        };

        $scope.benefit_type = 'Supplemental Life Insurance';

    }]);

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
        };

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
