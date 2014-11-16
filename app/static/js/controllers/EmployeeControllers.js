var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
    ['$scope', '$location', '$routeParams', 'employeeCompanyRoles', 'employeeBenefits', 'currentUser', 'userDocument',
    function employeeHome($scope, $location, $routeParams, employeeCompanyRoles, employeeBenefits, currentUser, userDocument){
    $('body').removeClass('onboarding-page');
    var curUserId;
    var userPromise = currentUser.get().$promise
      .then(function(response){
        $scope.employee_id = response.user.id;
        return response.user.id;
      });

    var companyPromise = userPromise.then(function(userId){
        curUserId = userId;
        return employeeCompanyRoles.get({userId:userId}).$promise;
    });

    var benefitPromise = companyPromise.then(function(response){
      var curCompanyId;
        _.each(response.company_roles, function(role){
          if (role.company_user_type === 'employee'){
            curCompanyId = role.company.id;
          }
        })
        return curCompanyId;
    });

    benefitPromise.then(function(companyId){
                        employeeBenefits.get({userId:curUserId, companyId:companyId})
                        .$promise.then(function(response){
                                       $scope.benefits = response.benefits;
                                       $scope.benefitCount = response.benefits.length;
                                       })
                        });

     var curUserPromise = currentUser.get().$promise.
         then(function(userResponse){
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
     }

  }
]);

var employeeBenefitSignup = employeeControllers.controller('employeeBenefitSignup', ['$scope', '$location', '$routeParams', 'employeeCompanyRoles', 'employeeBenefits', 'benefitListRepository', 'employeeFamily',
  function employeeBenefitController($scope, $location, $routeParams, employeeCompanyRoles, employeeBenefits, benefitListRepository, employeeFamily){

    var medicalPlans = [];
    var dentalPlans = [];
    var visionPlans = [];
    var employeeId = $routeParams.employee_id;
    var companyId;
    $scope.employee_id = employeeId;
    $scope.availablePlans = [];
    $scope.family = [];
    $scope.selectedBenefits =[];
    $scope.selectedBenefitHashmap = {};

    employeeFamily.get({userId:employeeId}).$promise
    .then(function(response){
      _.each(response.family, function(member){
        member.ticked = false;
        $scope.family.push(member);
      });
    });

    var companyIdPromise =  employeeCompanyRoles.get({userId:employeeId})
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
    var getEligibleFamilyMember = function(benefit, selected){
      var availFamilyList = {};
      var selectedMemberHash = {};
      if(selected)
      {
        _.each(selected.enrolleds, function(enrolled){
          selectedMemberHash[enrolled.id] = enrolled;
        });
      }
      switch(benefit.benefit_option_type)
      {
        case 'individual':
          availFamilyList.familyList = _.where(angular.copy($scope.family), {relationship:'self'});
          availFamilyList.eligibleNumber = 1;
        break;
        case 'individual_plus_spouse':
          availFamilyList.familyList = _.filter(angular.copy($scope.family), function(elem){
            return elem.relationship == 'self' || elem.relationship == 'spouse'});
          availFamilyList.eligibleNumber = 2;
        break;
        case 'individual_plus_one':
          availFamilyList.familyList = angular.copy($scope.family);
          availFamilyList.eligibleNumber = 2;
        break;
        case 'individual_plus_child':
          availFamilyList.familyList = _.filter(angular.copy($scope.family), function(elem){
            return elem.relationship == 'self' || elem.relationship == 'child'});
          availFamilyList.eligibleNumber = 2;
        break;
        default:
        case 'family':
          availFamilyList.familyList = angular.copy($scope.family);
          availFamilyList.eligibleNumber = $scope.family.length;
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
  companyIdPromise.then(function(companyId){
      employeeBenefits.get({userId:employeeId, companyId:companyId})
        .$promise.then(function(response){
          $scope.selectedBenefits = response.benefits;
          _.each($scope.selectedBenefits, function(benefitMember){
            $scope.selectedBenefitHashmap[benefitMember.benefit.id] = benefitMember.benefit;
          });
          benefitListRepository.get({clientId:companyId})
          .$promise.then(function(response){
            _.each(response.benefits, function(availBenefit){
              var benefitFamilyPlan = {benefit:availBenefit};
              var selectedBenefitPlan = _.first(_.filter($scope.selectedBenefits, function(selectedBen){
                return selectedBen.benefit.benefit_type == availBenefit.benefit_type;
              }));

              benefitFamilyPlan.eligibleMemberCombo = getEligibleFamilyMember(availBenefit, selectedBenefitPlan);
              var curTypePlan = _.findWhere($scope.availablePlans, {type:availBenefit.benefit_type});
              if(!curTypePlan)
              {
                curTypePlan = {type:availBenefit.benefit_type, benefitList:[], selected:{}};
                $scope.availablePlans.push(curTypePlan);
              }
              curTypePlan.benefitList.push(benefitFamilyPlan);
            });
            _.each($scope.availablePlans, function(typedPlan){
              _.each(typedPlan.benefitList, function(curBenefit){
                var retrievedBenefit = $scope.selectedBenefitHashmap[curBenefit.benefit.id];
                if(retrievedBenefit)
                {
                  typedPlan.selected = curBenefit;
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

    $scope.addMember = function(){
      $location.path('/employee/add_family/' + employeeId);
    };

    $scope.save = function(){
      var saveRequest = {benefits:[],waived:[]};
      var invalidEnrollNumberList = [];
      _.each($scope.availablePlans, function(benefitTypePlan){
        var enrolledList = [];
        _.each(benefitTypePlan.selected.eligibleMemberCombo.familyList, function(member){
          if(member.selected)
          {
            enrolledList.push({id:member.id});
          }
        });

        if(enrolledList.length > 0)
        {
          var requestBenefit = {benefit:{id:benefitTypePlan.selected.benefit.id,
              benefit_type:benefitTypePlan.selected.benefit.benefit_type},
            enrolleds:enrolledList};
          saveRequest.benefits.push(requestBenefit);

          if(benefitTypePlan.selected.benefit.benefit_option_type != 'family' &&
             requestBenefit.enrolleds.length < benefitTypePlan.selected.eligibleMemberCombo.eligibleNumber)
          {
            //validation failed.
            var invalidEnrollNumber = {};
            invalidEnrollNumber.name = benefitTypePlan.selected.benefit.benefit_name;
            invalidEnrollNumber.requiredNumber = benefitTypePlan.selected.eligibleMemberCombo.eligibleNumber;
            invalidEnrollNumberList.push(invalidEnrollNumber);
          }
        }
      });

      if(invalidEnrollNumberList.length > 0){
        alert("For benefit " + invalidEnrollNumberList[0].name +
                ", you have to elect " + invalidEnrollNumberList[0].requiredNumber + " family members!");
        return;
      }

      _.each($scope.selectedBenefits, function(benefitEnrolled){
          var matched = _.filter(saveRequest.benefits, function(uiSelected){
            return uiSelected.benefit.benefit_type == benefitEnrolled.benefit.benefit_type;
          })
          if(matched.length === 0)
          {
            saveRequest.waived.push({benefit_type:benefitEnrolled.benefit.benefit_type});
          }
        });

      employeeBenefits.save({userId: employeeId, companyId: companyId},
        saveRequest, function(){
          $location.path('/employee');
        }, function(){
          $scope.savedSuccess = false;
        });
    }
  }]);

var addFamily = employeeControllers.controller('addFamily', ['$scope', '$location', '$routeParams', 'employeeFamily',
  function addFamily($scope, $location, $routeParams, employeeFamily){

    var employeeId = $routeParams.employee_id;
    $scope.employeeId = employeeId;
  $scope.person = {};

  var mapPerson = function(viewPerson){
    if(typeof(viewPerson.address)=='undefined'){
      viewPerson.address={};
    }
    viewPerson.address.address_type = 'home';
    if(typeof(viewPerson.phone)=='undefined'){
      viewPerson.phone = {};
    }
    viewPerson.phone.phone_type = 'home';
    var apiPerson = {};
    apiPerson.full_name = viewPerson.full_name;
    apiPerson.birth_date = viewPerson.birth_date;
    apiPerson.ssn = viewPerson.ssn;
    apiPerson.relationship = viewPerson.relationship;
    apiPerson.addresses = [];
    apiPerson.addresses.push(viewPerson.address);
    apiPerson.phones = [];
    apiPerson.phones.push(viewPerson.phone);
    return {person: apiPerson};
  }


  $scope.addMember = function(){
    var viewPerson = $scope.person;
    var apiPerson = mapPerson(viewPerson);
    employeeFamily.save({userId:employeeId}, apiPerson, function(){
      $location.path('/employee/benefit/' + employeeId);
    }, function(){
      $scope.saveSucceed = false;
    })
  }
}]);


var viewDocument = employeeControllers.controller('viewDocument',
  ['$scope', '$location', '$routeParams', 'userDocument', 'currentUser', 'documentRepository',
  function viewDocument($scope, $location, $routeParams, userDocument, currentUser, documentRepository){
    $scope.document = {};
    var documentId = $routeParams.doc_id;
    var signatureUpdated = false;
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
        $scope.signatureImage = document.signature.signature;
        $scope.signaturePresent = true;
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
      $sigdiv.jSignature("reset")
    };
    $scope.signDocument = function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        var signaturePayload = "data:" + signatureData[0] + ',' + signatureData[1];
        documentRepository.sign.save({id:$scope.document.id}, {'signature':signaturePayload}, function(successResponse){
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
    }

}]);

var signIn = employeeControllers.controller('employeeSignin', ['$scope', '$routeParams', function($scope, $routeParams){
  $scope.employee = {};
  $scope.employee.id = $routeParams.employee_id;
  $scope.employee.username = '';
  $scope.employee.password = '';

  $scope.submit = function(employee) {
    // Need to add actions to validate sign in credentials
    return false;
  }
}]);

var signup = employeeControllers.controller('employeeSignup', ['$scope', '$routeParams', '$location',
  function($scope, $routeParams, $location){
    $scope.employee = {};
    $scope.employee.id = $routeParams.signup_number;

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
  ['$scope', '$routeParams', '$location', 'employeeFamily', 'currentUser',
  function($scope, $routeParams, $location, employeeFamily, currentUser){
    $('body').addClass('onboarding-page');
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
    currentUser.get()
      .$promise.then(function(curUserResponse){
        $scope.curUser = curUserResponse.user;
      }); 
    var mapEmployee = function(viewEmployee){
      var apiEmployee = {
        'person_type': 'family',
        'relationship': 'self',
        'first_name': viewEmployee.firstName,
        'last_name': viewEmployee.lastName,
        'birth_date': viewEmployee.birth_date,
        'ssn': viewEmployee.ssn,
        'email': $scope.curUser.email,
        'addresses': [],
        'phones': [
          {
            'phone_type': 'home',
            'number': viewEmployee.phone.number
          }
        ]
      };

      viewEmployee.address.address_type = 'home';
      apiEmployee.addresses.push(viewEmployee.address);
      return apiEmployee;
    };

    $scope.addBasicInfo = function(){
      var newEmployee = mapEmployee($scope.employee);
      employeeFamily.save({userId: $scope.employeeId}, newEmployee,
        function(){
          $location.path('/employee/onboard/employment/' + $scope.employeeId);
        }, function(){
          alert('Failed to add the new user');
        });
    };
}]);

var onboardEmployment = employeeControllers.controller('onboardEmployment',
  ['$scope', '$routeParams', '$location', 'employeeOnboarding',
  function($scope, $routeParams, $location, employeeOnboarding){
    $('body').addClass('onboarding-page');
    $scope.employee = {

    };
    $scope.employeeId = $routeParams.employee_id;

    var mapContract = function(viewObject, signature){
      var contract = {
        'worker_type': viewObject.auth_type,
        'expiration_date': viewObject.auth_expiration,
        'uscis_number': viewObject.authNumber,
        'i_94': viewObject.I94Id,
        'passport': viewObject.passportId,
        'country': viewObject.passportCountry,
        'signature': {
          'signature': signature,
          'signature_type': 'step'
        }
      };
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
      $sigdiv.jSignature("reset")
    };
    $scope.signDocument = function(){
      if(!signatureUpdated){
        alert('Please sign your name on the signature pad');
      }
      else
      {
        var signatureData = $sigdiv.jSignature('getData', 'svg');
        $scope.signatureImage = "data:" + signatureData[0] + ',' + signatureData[1];
        var contract = mapContract($scope.employee, $scope.signatureImage);
        employeeOnboarding.save({userId: $scope.employeeId}, contract,
          function(){
            $location.path('/employee/onboard/tax/' + $scope.employeeId);
          }, function(){
            alert('Failed to add employment information');
          });
      }
    }
}]);

var onboardTax = employeeControllers.controller('onboardTax',
  ['$scope', '$routeParams', '$location',
  function($scope, $routeParams, $location){
    $('body').addClass('onboarding-page');
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
    $scope.employee.withholdingType = 'single';
    $scope.employee.headOfHousehold = 0;
    $scope.employee.childExpense = 0;
    $scope.submit=function(){
      $location.path('/employee/onboard/complete/'+$scope.employeeId);
    }
}]);

var onboardComplete = employeeControllers.controller('onboardComplete',
  ['$scope', '$routeParams', '$location', 'employeeSignature',
  function($scope, $routeParams, $location, employeeSignature){
    $('body').addClass('onboarding-page');
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
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
      $sigdiv.jSignature("reset")
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
}])

