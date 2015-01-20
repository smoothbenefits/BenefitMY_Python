var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
    ['$scope',
     '$location',
     '$routeParams',
     'clientListRepository',
     'employeeBenefits',
     'currentUser',
     'userDocument',
     'EmployeePreDashboardValidationService',
     'EmployeeLetterSignatureValidationService',
  function employeeHome($scope,
                        $location,
                        $routeParams,
                        clientListRepository,
                        employeeBenefits,
                        currentUser,
                        userDocument,
                        EmployeePreDashboardValidationService,
                        EmployeeLetterSignatureValidationService){

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
          })
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
          })
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

     $scope.ViewInfo = function(type){
      $location.path('/employee/info').search('type', type);
     }
  }
]);

var employeeBenefitSignup = employeeControllers.controller(
  'employeeBenefitSignup',
  ['$scope',
   '$location',
   '$routeParams',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'employeeFamily',
   'benefitDisplayService',
    function employeeBenefitController(
      $scope,
      $location,
      $routeParams,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      employeeFamily,
      benefitDisplayService){

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

        var companyIdPromise =  clientListRepository.get({userId:employeeId})
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
                return elem.relationship == 'self' || elem.relationship == 'child'});
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

        companyIdPromise.then(function(companyId){
          benefitDisplayService(companyId, true, function(groupObj, nonMedicalArray, benefitCount){
            $scope.medicalBenefitGroup = groupObj;
            $scope.nonMedicalBenefitArray = nonMedicalArray;
          });
          employeeBenefits.enroll().get({userId:employeeId, companyId:companyId})
            .$promise.then(function(response){
              $scope.selectedBenefits = response.benefits;
              _.each($scope.selectedBenefits, function(benefitMember){
                benefitMember.benefit.pcp = benefitMember.pcp;
                $scope.selectedBenefitHashmap[benefitMember.benefit.id] = benefitMember.benefit;
              });
              benefitListRepository.get({clientId:companyId})
              .$promise.then(function(response){
                _.each(response.benefits, function(availBenefit){
                  var benefitFamilyPlan = {benefit:availBenefit};
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
                    curTypePlan = {type:availBenefit.benefit_type, benefitList:[], selected:{}};

                    var waiveOption = {
                                        benefit: {
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
                _.each($scope.availablePlans, function(typedPlan){
                  _.each(typedPlan.benefitList, function(curBenefit){
                    var retrievedBenefit = $scope.selectedBenefitHashmap[curBenefit.benefit.id];
                    if(retrievedBenefit)
                    {
                      typedPlan.selected = curBenefit;
                      typedPlan.selected.pcp = retrievedBenefit.pcp;
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

        $scope.isMedicalBenefitType = function(benefit){
          return benefit && benefit.benefit_type === 'Medical';
        };

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
                  enrolledList.push({id:member.id});
                }
              });
            }

            if(enrolledList.length > 0)
            {
              var requestBenefit = {
                benefit:{
                  id:benefitTypePlan.selected.benefit.id,
                  benefit_type:benefitTypePlan.selected.benefit.benefit_plan.benefit_type.name,
                  pcp:benefitTypePlan.selected.pcp
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
                var type = benefitPlan.benefit_type;
                //This code below is such an hack. We need to get the type key from the server!
                //CHANGE THIS
                var typeKey = 0;
                if (type === 'Medical'){
                  typeKey = 1;
                }
                if (type === 'Dental'){
                  typeKey = 2;
                }
                if (type === 'Vision'){
                  typeKey = 3;
                }
                saveRequest.waivedRequest.waived.push({benefit_type: typeKey, type_name: type});
              }
            });

          employeeBenefits.waive().save({userId: employeeId}, saveRequest.waivedRequest, function(){}, 
             function(errorResponse){
              alert('Saving waived selection failed because: ' + errorResponse.data);
              $scope.savedSuccess = false;
            });
        

          employeeBenefits.enroll().save({userId: employeeId, companyId: companyId}, saveRequest, function(){
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
    apiPerson.emergency_contact=[];
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
        var signature = document.signature.signature;
        var separator = '<?xml';
        var sigComponents = signature.split(separator);
        $scope.signatureImage = sigComponents[0] + encodeURIComponent(separator + sigComponents[1]);
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
    }

}]);

var employeeInfo = employeeControllers.controller('employeeInfoController',
  ['$scope', '$location', '$routeParams', 'profileSettings', 'currentUser', 'employmentAuthRepository', 'employeeTaxRepository',
  function($scope, $location, $routeParams, profileSettings, currentUser, employmentAuthRepository, employeeTaxRepository){
    var infoObject = _.findWhere(profileSettings, { name: $routeParams.type });
    $scope.info = { type: $routeParams.type, type_display: infoObject.display_name };
    $scope.person = { role: 'Employee' };

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
  ['$scope', '$routeParams', '$location', 'selfInfoService', 'currentUser', 'EmployeePreDashboardValidationService',
  function($scope, $routeParams, $location, selfInfoService, currentUser, EmployeePreDashboardValidationService){

    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;
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
      selfInfoService.saveSelfInfo($scope.employeeId, $scope.employee, function(successResponse){
        $location.path('/employee/onboard/employment/' + $scope.employeeId);
      }, function(errorResponse){
          alert('Failed to add the new user. The error is: ' + JSON.stringify(errorResponse.data) +'\n and the http status is: ' + errorResponse.status);
      });
    };
}]);

var onboardEmployment = employeeControllers.controller('onboardEmployment',
  ['$scope', '$routeParams', '$location', 'employmentAuthRepository', 'EmployeePreDashboardValidationService',
  function($scope, $routeParams, $location, employmentAuthRepository, EmployeePreDashboardValidationService){
    $scope.employee = {

    };
    $scope.employeeId = $routeParams.employee_id;

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
      var expirationDate = moment(viewObject.auth_expiration);
      var contract = {
        'worker_type': viewObject.auth_type,
        'expiration_date': expirationDate.format('YYYY-MM-DD'),
        'uscis_number': viewObject.authNumber,
        'i_94': viewObject.I94Id,
        'passport': viewObject.passportId,
        'country': viewObject.passportCountry,
        'signature': {
          'signature': signature,
          'signature_type': 'work_auth'
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
        $scope.signatureImage = "data:" + signatureData[0] + ',' + signatureData[1];
        var contract = mapContract($scope.employee, $scope.signatureImage);
        employmentAuthRepository.save({userId: $scope.employeeId}, contract,
          function(){
            $location.path('/employee/onboard/tax/' + $scope.employeeId);
          }, function(){
            alert('Failed to add employment information');
          });
      }
    }
}]);

var onboardTax = employeeControllers.controller('onboardTax',
  ['$scope', '$routeParams', '$location','employeeTaxRepository', 'EmployeePreDashboardValidationService',
  function($scope, $routeParams, $location, employeeTaxRepository, EmployeePreDashboardValidationService){
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;

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
  ['$scope', '$routeParams', '$location', 'employeeSignature', 'EmployeePreDashboardValidationService',
  function($scope, $routeParams, $location, employeeSignature, EmployeePreDashboardValidationService){
    $scope.employee = {};
    $scope.employeeId = $routeParams.employee_id;

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
  ['$scope', '$routeParams', '$location', 'documentRepository', 'EmployeeLetterSignatureValidationService',
  function($scope, $routeParams, $location, documentRepository, EmployeeLetterSignatureValidationService){
    $scope.employeeId = $routeParams.employee_id;
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

