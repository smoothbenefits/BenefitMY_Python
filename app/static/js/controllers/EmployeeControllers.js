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

    employeeFamily.get({userId:employeeId}).$promise.then(function(response){
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
                curTypePlan = {type:availBenefit.benefit_type, benefitList:[], selected:{}};
                $scope.availablePlans.push(curTypePlan);
              }
              curTypePlan.benefitList.push(benefitFamilyPlan);
              curTypePlan.benefit_type = benefitType;
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
        if (typeof benefitTypePlan.selected.eligibleMemberCombo != 'undefined'){
          _.each(benefitTypePlan.selected.eligibleMemberCombo.familyList, function(member){
            if(member.selected)
            {
              enrolledList.push({id:member.id});
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
    apiPerson.person_type = "family";
    apiPerson.email = viewPerson.email;
    apiPerson.first_name = viewPerson.first_name;
    apiPerson.last_name = viewPerson.last_name;
    apiPerson.birth_date = viewPerson.birth_date;
    apiPerson.ssn = viewPerson.ssn;
    apiPerson.relationship = viewPerson.relationship;
    apiPerson.addresses = [];
    viewPerson.address.state = viewPerson.address.state.toUpperCase();
    apiPerson.addresses.push(viewPerson.address);
    apiPerson.phones = [];
    apiPerson.phones.push(viewPerson.phone);
    return apiPerson;
  }


  $scope.addMember = function(){
    var viewPerson = $scope.person;
    var apiPerson = mapPerson(viewPerson);
    employeeFamily.save({userId:employeeId}, apiPerson, function(){
      $location.path('/employee/benefit/' + employeeId);
    }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
    });
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
  ['$scope', '$routeParams', '$location', 'employeeFamily', 'currentUser', 'employeeOnboarding', 'employeeTaxRepository', 'employeeSignature', 'peopleRepository',
  function($scope, $routeParams, $location, employeeFamily, currentUser, employeeOnboarding, employeeTaxRepository, employeeSignature, peopleRepository){
    
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
    $scope.displayAll = false;
    var employmentAuthValidated = false;
    var taxValidated = false;
    var userPromise = currentUser.get()
      .$promise.then(function(curUserResponse){
        $scope.curUser = curUserResponse.user;
        return curUserResponse.user;
      });

    var validateBasicInfo = function(person){
      //make sure we get all the basic information of this person correctly.
      if(!person)
      {
        return false;
      }
      if(!person.email){
        return false;
      }
      if(!(person.first_name && person.last_name))
      {
        return false;
      }
      if(!person.birth_date)
      {
        return false;
      }
      if(!person.phones || person.phones.length <=0){
        return false;
      }
      if(!person.addresses || person.addresses.length <= 0){
        return false;
      }
      return true;
    };

    var getEmploymentAuthUrl = function(employeeId){
      return '/employee/onboard/employment/' + employeeId;
    };

    var getTaxUrl = function(employeeId){
      return '/employee/onboard/tax/' + employeeId;
    };

    var getSignatureUrl = function(employeeId){
      return '/employee/onboard/complete/' + employeeId;
    };

    var getOnboardStartingUrl = function(employeeId){
      //We would like to check if this user has the correct information for each steps
      //starting from the basic information check

      //step one (basic info) validation
      employeeFamily.get({userId:employeeId})
        .$promise.then(function(familyResponse){
          var self = _.findWhere(familyResponse.family, {'relationship':'self'});
          if(self){
            //We need to validate this self
            if(!validateBasicInfo(self)){
            //we should remove the family person.
            //Do we have this API?
              peopleRepository.delete({personId:self.id});
              $scope.displayAll = true;
            }
          }
          else{
            $scope.displayAll = true;
          }
        });
      //step two (employment auth) validation
      //get the sigature for employment auth document
      employeeOnboarding.get({userId:employeeId})
        .$promise.then(function(response){
           if(!(response && response.signature && response.signature.signature)){
            if(!$scope.displayAll){
              $location.path(getEmploymentAuthUrl(employeeId));
            }
           }
           else{
            employmentAuthValidated = true;
           }
        });
    
      employeeTaxRepository.get({userId:employeeId})
        .$promise.then(function(response){
          if(!response || !response.total_points || response.total_points <= 0){
            if(!$scope.displayAll && employmentAuthValidated){
              $location.path(getTaxUrl(employeeId));
            }
          }
          else{
            taxValidated = true;
          }
        }, function(err){
          if(!$scope.displayAll && employmentAuthValidated){
            $location.path(getTaxUrl(employeeId));
          }
        });
    
      if(!$scope.displayAll){
        //step 4 the signature for employee
        employeeSignature.get({userId:employeeId})
          .$promise.then(function(signature){
            if(!signature || !signature.signature || signature.signature===''){
              if(!$scope.displayAll && employmentAuthValidated && taxValidated){
                $location.path(getSignatureUrl(employeeId));
              }
            }
            else{
              //we have finished all the validation.
              $location.path('/employee');
            }
          })
      }
    };

    getOnboardStartingUrl($scope.employeeId);

    $('body').addClass('onboarding-page');

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
      viewEmployee.address.state = viewEmployee.address.state.toUpperCase();
      apiEmployee.addresses.push(viewEmployee.address);
      return apiEmployee;
    };

    $scope.addBasicInfo = function(){
      var newEmployee = mapEmployee($scope.employee);
      employeeFamily.save({userId: $scope.employeeId}, newEmployee,
        function(){
          $location.path('/employee/onboard/employment/' + $scope.employeeId);
        }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
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
          'signature': signature
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
  ['$scope', '$routeParams', '$location','employeeTaxRepository',
  function($scope, $routeParams, $location, employeeTaxRepository){
    $('body').addClass('onboarding-page');
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
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

    var getTotalPoints = function(){
      var total = getMarriageNumber() + 1;
      total += $scope.employee.dependent_count;
      if($scope.employee.childExpense){
        total ++;
      }
      return total;
    };

    $scope.submit=function(){
      var empAuth = {
        marriage: getMarriageNumber(),
        dependencies: $scope.employee.dependent_count,
        head: $scope.employee.headOfHousehold,
        tax_credit: $scope.employee.childExpense,
        total_points: getTotalPoints()
      };
      employeeTaxRepository.save({userId:$scope.employeeId}, empAuth,
        function(response){
          $location.path('/employee/onboard/complete/'+$scope.employeeId);
        }); 
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

