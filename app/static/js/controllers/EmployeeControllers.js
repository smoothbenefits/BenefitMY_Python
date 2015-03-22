var employeeControllers = angular.module('benefitmyApp.employees.controllers',[]);

var employeeHome = employeeControllers.controller('employeeHome',
    ['$scope',
     '$location',
     '$stateParams',
     'clientListRepository',
     'employeeBenefits',
     'currentUser',
     'userDocument',
     'EmployeePreDashboardValidationService',
     'EmployeeLetterSignatureValidationService',
     'FsaService',
     'LifeInsuranceService',
  function employeeHome($scope,
                        $location,
                        $stateParams,
                        clientListRepository,
                        employeeBenefits,
                        currentUser,
                        userDocument,
                        EmployeePreDashboardValidationService,
                        EmployeeLetterSignatureValidationService,
                        FsaService,
                        LifeInsuranceService){

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
     };

     $scope.ViewInfo = function(type){
      $location.path('/employee/info').search('type', type);
     };

     $scope.EditInfo = function(type){
      $location.path('/employee/info/edit').search('type', type);
     };

    // FSA election data
    curUserPromise.then(function(userId) {
      FsaService.getFsaElectionForUser(userId, function(response) {
        $scope.fsaElection = response;
      });
    });

    // Life Insurance
    curUserPromise.then(function(userId) {
      LifeInsuranceService.getInsurancePlanEnrollmentsForAllFamilyMembersByUser(userId, function(response) {
        $scope.familyInsurancePlan = response;
      });

      LifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(userId, function(response){
        $scope.basicLifeInsurancePlan = response;
        $scope.basicLifeInsurancePlan.life_insurance.last_update_date = moment(response.life_insurance.updated_at).format('l');
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

var employeeBenefitSignup = employeeControllers.controller(
  'employeeBenefitSignup',
  ['$scope',
   '$location',
   '$stateParams',
   'clientListRepository',
   'employeeBenefits',
   'benefitListRepository',
   'employeeFamily',
   'benefitDisplayService',
   'FsaService',
   'LifeInsuranceService',
    function employeeBenefitController(
      $scope,
      $location,
      $stateParams,
      clientListRepository,
      employeeBenefits,
      benefitListRepository,
      employeeFamily,
      benefitDisplayService,
      FsaService,
      LifeInsuranceService){

        var medicalPlans = [];
        var dentalPlans = [];
        var visionPlans = [];
        var employeeId = $stateParams.employee_id;
        var companyId;
        $scope.employee_id = employeeId;
        $scope.availablePlans = [];
        $scope.family = [];
        $scope.selectedBenefits =[];
        $scope.selectedBenefitHashmap = {};

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

        companyIdPromise.then(function(companyId){
          benefitDisplayService(companyId, false, function(groupObj, nonMedicalArray, benefitCount){
            $scope.medicalBenefitGroup = groupObj;
            $scope.nonMedicalBenefitArray = nonMedicalArray;
          });

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

        // Life Insurance 
        $scope.lifeInsurancePlans = [ { text: '<Waive Life Insurance>', value: '0' } ];
        $scope.selectedLifeInsurancePlan = $scope.lifeInsurancePlans[0];

        companyIdPromise.then(function(companyId){
          LifeInsuranceService.getLifeInsurancePlansForCompany(companyId, function(plans) {

            // Populate available company plans
            _.each(plans, function(plan) {
              // separate basic life insurance from supplemental life insurance.
              // for now, it will pick the last basic life insurance defined by broker.
              if (plan.life_insurance_plan.insurance_type === 'Basic'){
                $scope.basicLifeInsurancePlan = plan;
                $scope.basicLifeInsurancePlan.selected = true;
              }
              else{
                $scope.lifeInsurancePlans.push({ text: plan.life_insurance_plan.name, value: plan.id });  
              }
            });

            // Get current user's basic life insurance plan situation
            LifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employeeId, function(plan){
              $scope.basicLifeInsurancePlan.life_insurance_beneficiary = plan.life_insurance_beneficiary;
              $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary = plan.life_insurance_contingent_beneficiary;
            }, function(error){
              $scope.error = true;
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

        // User should be able to add up to 4 beneficiaries of life insurance
        $scope.addBeneficiary = function(){
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.push({});
        };

        $scope.addBeneficiaryToBasic = function(){
          if (!$scope.basicLifeInsurancePlan.life_insurance_beneficiary){
            $scope.basicLifeInsurancePlan.life_insurance_beneficiary = []
          }
          $scope.basicLifeInsurancePlan.life_insurance_beneficiary.push({});
        };

        $scope.addContingentBeneficiary = function(){
          if (!$scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary){
            $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary = [];
          }
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.push({});
        };

        $scope.addContingentBeneficiaryToBasic = function(){
          if (!$scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary){
            $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary = []
          }
          $scope.basicLifeInsurancePlan.life_insurance_contingent_beneficiary.push({});
        };

        $scope.removeBeneficiary = function(beneficiary){
          var index = $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.indexOf(beneficiary);
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_beneficiary.splice(index, 1);
        };

        $scope.removeContingentBeneficiary = function(beneficiary){
          var index = $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.indexOf(beneficiary);
          $scope.familyLifeInsurancePlan.mainPlan.life_insurance_contingent_beneficiary.splice(index, 1);
        };

        $scope.removeFromList = function(item, list){
          var index = list.indexOf(item);
          list.splice(index, 1);
        };

        $scope.isMedicalBenefitType = function(benefit){
          return benefit && benefit.benefit_type === 'Medical';
        };

        $scope.isWaived = function(selectedPlan){
          if (!selectedPlan.benefit){
            return true;
          }
          return selectedPlan.benefit.benefit_plan.name.toLowerCase() === 'waive';
        };

        $scope.medicalWaiveReasons = [
          'I am covered under another plan as a spouse or dependent',
          'I am covered by MassHealth, Medicare, Commonwealth Health Connector plan, non-group, or Veterans program',
          'I am covered under another plan sponsored by a second employer',
          'I am covered by another health plan sponsored by this employer'
        ];

        // Whether the user has selected a reason for updating 
        // his/her FSA configuration.
        $scope.isFsaUpdateReasonSelected = function() {
          return $scope.selectedFsaUpdateReason.value > 0;
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
                  $location.path('/employee/benefit/' + $scope.employee_id);
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
              $location.path('/employee');
            }, function(){
              $scope.savedSuccess = false;
            });

          // Save FSA selection if user specifies a reason
          if ($scope.isFsaUpdateReasonSelected()){
            $scope.fsaElection.update_reason = $scope.selectedFsaUpdateReason.text;
            FsaService.saveFsaElection($scope.fsaElection, null, function() {
              $scope.savedSuccess = false;
            });
          }

          // Save life insurance
          if ($scope.isWaiveLifeInsuranceSelected()) {
            // Waive selected. Delete all user plans for this user
            LifeInsuranceService.deleteFamilyLifeInsurancePlanForUser(employeeId, null, function(error) {
              $scope.savedSuccess = false;
            });
          } else {
            $scope.familyLifeInsurancePlan.selectedCompanyPlan = $scope.selectedLifeInsurancePlan.value;
            LifeInsuranceService.saveFamilyLifeInsurancePlanForUser($scope.familyLifeInsurancePlan, null, function(error) {
              $scope.savedSuccess = false;
              alert('Failed to save your beneficiary information. Please make sure all required fields have been filled.');
            });
          }

          ///////////////////////////////////////////////////////////////////////////
          // Save basic life insurance
          // TO-DO: Need to better organize the logic to save basic life insurance
          ///////////////////////////////////////////////////////////////////////////
          if (!$scope.basicLifeInsurancePlan.selected){
            LifeInsuranceService.deleteBasicLifeInsurancePlanForUser(employeeId, null, function(error) {
              $scope.savedSuccess = false;
            });
          }
          else{
            LifeInsuranceService.getInsurancePlanEnrollmentsByUser(employeeId, function(enrolledPlans){
              var enrolledBasic = _.find(enrolledPlans, function(plan){ 
                return plan.life_insurance.life_insurance_plan.insurance_type === 'Basic';
              });
              if (enrolledBasic){
                $scope.basicLifeInsurancePlan.enrolled = true;
                $scope.basicLifeInsurancePlan.id = enrolledBasic.id;
              }
              else{
                $scope.basicLifeInsurancePlan.enrolled = false;
              }
              
              $scope.basicLifeInsurancePlan.currentUserId = employeeId;

              LifeInsuranceService.saveBasicLifeInsurancePlanForUser($scope.basicLifeInsurancePlan, null, function(error){
                $scope.savedSuccess = false;
                alert('Failed to save basic life insurance. Please make sure all required fields have been filled.')
              });
            }, function(error) {
              $scope.savedSuccess = false;
            });
          }
        };
      }]);

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
      $location.path('/employee/benefit/' + employeeId);
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
    $scope.signatureCreatedDate = moment().format('MMM Do YYYY');
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
        $scope.signatureCreatedDate = moment(document.signature.created_at).format('MMM Do YYYY');
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
   '$routeParams',
   '$location',
   'currentUser',
   'DirectDepositService',
   function($scope, 
            $routeParams,
            $location,
            currentUser,
            DirectDepositService){
    $scope.editMode = $routeParams.edit;
    $scope.person = { role: 'Employee' };
    $scope.direct_deposit = { bank_accounts: [] };
    $scope.bankAccountTypes = ['Checking', 'Saving'];

    $scope.enableEditing = function(){
      $scope.editMode = true;
    };

    $scope.backToDashboard = function(){
      $location.path('/employee');
    };

    $scope.removeBankAccount = function(account){
      var index = $scope.direct_deposit.bank_accounts.indexOf(account);
      $scope.direct_deposit.bank_accounts.splice(index, 1);
    };

    $scope.addBankAccount = function(){
      $scope.direct_deposit.bank_accounts.push({ account_type: $scope.bankAccountTypes[0]});
    };

    var userPromise = currentUser.get().$promise.then(function(response){
      $scope.person = response.user;
      return response.user.id;
    });

    userPromise.then(function(userId){
      DirectDepositService.getDirectDepositByUserId(userId, function(response){
        $scope.direct_deposit.bank_accounts = response;
        if (response.length === 0){
          $scope.hasDirectDeposit = false;
          $scope.direct_deposit.bank_accounts.push({ account_type: $scope.bankAccountTypes[0]});
        }
        else {
          $scope.hasDirectDeposit = true;
        }
      });
    });

    $scope.submitDirectDeposit = function(){
      var request_body = { user: $scope.person.id, bank_account: $scope.direct_deposit.bank_accounts };
      if ($scope.hasDirectDeposit){
        DirectDepositService.updateDirectDepositByUserId($scope.person.id, request_body, function(response){
          $location.path('/employee');
        }, function(error){
          alert('Failed to save direct deposit information due to ' + error);
        });
      }
      else{
        DirectDepositService.createDirectDepositByUserId($scope.person.id, request_body, function(response){
          $location.path('/employee');
        }, function(error){
          alert('Failed to create direct deposit record due to ' + error);
        });
      }
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
    }

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
    }
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
