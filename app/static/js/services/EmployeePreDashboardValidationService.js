var benefitmyService = angular.module('benefitmyService');


benefitmyService.factory('EmployeePreDashboardValidationService',
                         ['$state',
                          'PersonService',
                          'UserService',
                          'employmentAuthRepository',
                          'employeeTaxRepository',
                          'PersonService',
                          'DocumentService',
                          'BenefitSummaryService',
                          'CompanyFeatureService',
                          'DirectDepositService',
                          'UserOnboardingStepStateService',
                          'OpenEnrollmentDefinitionService',
                          'EmployeeTaxElectionService',
  function($state,
           PersonService,
           UserService,
           employmentAuthRepository,
           employeeTaxRepository,
           PersonService,
           DocumentService,
           BenefitSummaryService,
           CompanyFeatureService,
           DirectDepositService,
           UserOnboardingStepStateService,
           OpenEnrollmentDefinitionService,
           EmployeeTaxElectionService){

    var getUrlFromState = function(state, stateParams) {
        return $state.href(state, stateParams).replace('#', '').replace('!', '');
    };

    var getBasicInfoUrl = function(employeeId){
      return getUrlFromState('employee_onboard.basic_info', { employee_id: employeeId });
    };

    var getEmploymentAuthUrl = function(employeeId){
      return getUrlFromState('employee_onboard.employment', { employee_id: employeeId });
    };

    var getTaxUrl = function(employeeId){
      return getUrlFromState('employee_onboard.tax', { employee_id: employeeId });
    };

    var getStateTaxUrl = function(employeeId){
      return getUrlFromState('employee_onboard.state_tax', { employee_id: employeeId });
    };

    var getDocumentUrl = function(employeeId){
      return getUrlFromState('employee_onboard.document', { employee_id: employeeId });
    };

    var getDirectDepositUrl = function(employeeId){
      return getUrlFromState('employee_onboard.direct_deposit', { employee_id: employeeId });
    };

    var getBenefitEnrollFlowUrl = function(employeeId){
      return getUrlFromState('employee_family', { employeeId: employeeId });
    };

    var validatePersonInfo = function(person){
      //make sure we get all the basic information of this person correctly.
      if(!person)
      {
        return false;
      }
      if(!(person.first_name && person.last_name))
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

    var validateBasicInfo = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed){
      //step one (basic info) validation
      PersonService.getSelfPersonInfo(employeeId)
        .then(function(self){
          if(self){
            //We need to validate this self
            if(!validatePersonInfo(self)){
              failed();
            }
            else{
              succeeded();
            }
          }
          else{
            failed();
          }
        }, function(){
          failed();
        });
    };

    var validateEmploymentAuth = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed){
      if (!isNewEmployee 
        || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.I9)) {
        // Skip I-9 validation if this is not a new employee
        succeeded();
      } 
      else {
        //step two (employment auth) validation
        //get the sigature for employment auth document
        employmentAuthRepository.get({userId:employeeId})
        .$promise.then(function(response){
           if(!(response && response.signature && response.signature.signature)){
            failed();
           }
           else{
            succeeded();
           }
        },function(error){
          if(failed){
            failed();
          }
        });
      } 
    };

    var validateW4Info = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed){
      if (!isNewEmployee 
        || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.W4)) {
        // Skip W-4 validation if this is not a new employee
        succeeded();
      } 
      else {
        employeeTaxRepository.get({userId:employeeId})
        .$promise.then(function(response){
          if(!response ||
             (_.isNumber(response.user_defined_points) && response.user_defined_points < 0) ||
             (_.isNumber(response.total_points) && response.total_points < 0)){
            //For backwards compatibility, we need to check both fields.
            failed(response);
          }
          else{
            succeeded(response);
          }
        }, function(err){
          failed(err);
        });
      }
    };

    var validateStateTaxInfo = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed){
      if (!isNewEmployee 
        || !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.W4)) {
        // Skip State Tax validation if this is not a new employee, or if the feature switch is off
        succeeded();
      } 
      else {
        UserOnboardingStepStateService.checkUserFinishedStep(
            employeeId,
            UserOnboardingStepStateService.Steps.StateTaxInfo).then(
            function(stepFinishedAlreadyFlag) {
                if (stepFinishedAlreadyFlag) {
                    succeeded();
                }
                else {
                    EmployeeTaxElectionService.getTaxElectionsByEmployee(employeeId).then(
                        function(elections) {
                            if (elections && elections.length > 0) {
                                succeeded();
                            } else {
                                failed();
                            }
                        },
                        function(errors) {
                            failed();
                        }
                    );
                }
            },
            function(errors) {
                failed();
            }
        );
      }
    };

    var validateDirectDeposit = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed){
      if (!isNewEmployee ||
          !allFeatureStatus.isFeatureEnabled(CompanyFeatureService.AppFeatureNames.DD)) {
        // Skip if the feature is disabled or it's an existing employee
        succeeded();
      } 
      else {
        UserOnboardingStepStateService.checkUserFinishedStep(
            employeeId,
            UserOnboardingStepStateService.Steps.DirectDeposit).then(
            function(stepFinishedAlreadyFlag) {
                if (stepFinishedAlreadyFlag) {
                    succeeded();
                }
                else {
                    DirectDepositService.getDirectDepositByUserId(employeeId).then(
                        function(accounts) {
                            if (accounts && accounts.length > 0) {
                                succeeded();
                            }
                            else {
                                failed();
                            }
                        },
                        function(errors) {
                            failed();
                        }
                    );
                }
            },
            function(errors) {
                failed();
            } 
        );
      }
    };

    var validateDocuments = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed) {
        DocumentService.getAllDocumentsForUser(employeeId).then(
            function(documents) {
                if (!documents || documents.length <= 0) {
                    // No documents assumes success
                    succeeded();
                } else {
                    var notSigned = _.find(documents, function(doc) {
                        return !doc.signature;
                    });
                    if (!notSigned) {
                        succeeded();
                    } else {
                        failed();
                    }
                }
            },
            function(errors) {
                failed();
            }
        );
    };

    var validateBenefitEnrollmentCompleted = function(employeeId, companyId, succeeded, failed){
      BenefitSummaryService.getBenefitEnrollmentByUser(employeeId, companyId).then(
          function(enrollmentSummary) {
              if (enrollmentSummary.allEnrollmentsCompleted) {
                  succeeded();
              }
              else {
                  failed();
              }
          },
          function(errors) {
              failed();
          }
      );
    };

    var validateBenefitEnrollments = function(employeeId, isNewEmployee, allFeatureStatus, succeeded, failed) {
      UserService.getCurUserInfo().then(
        function(userInfo) {
          var company = userInfo.currentRole.company;
          if(isNewEmployee){
            validateBenefitEnrollmentCompleted(employeeId, company.id, succeeded, failed);
          }
          else{
            OpenEnrollmentDefinitionService.InOpenEnrollmentPeriod(company.id)
            .then(function(answer){
              if(answer){
                validateBenefitEnrollmentCompleted(employeeId, company.id, succeeded, failed);
              }
              else{
                succeeded();
              }
            }, function(error){
              succeeded();
            });
          }
        });
    };

    return {
        onboarding: function(employeeId, succeeded, failed){
          UserService.getCurrentRoleCompleteFeatureStatus().then(
            function(allFeatureStatus){
              UserService.isCurrentUserNewEmployee().then(
                function(isNewEmployee) {
                  validateBasicInfo(employeeId, isNewEmployee, allFeatureStatus, function(){
                    validateEmploymentAuth(employeeId, isNewEmployee, allFeatureStatus, function(){
                      validateW4Info(employeeId, isNewEmployee, allFeatureStatus, function(){
                        validateStateTaxInfo(employeeId, isNewEmployee, allFeatureStatus, function(){
                            validateDirectDeposit(employeeId, isNewEmployee, allFeatureStatus, function(){
                                validateDocuments(employeeId, isNewEmployee, allFeatureStatus, function() {
                                    validateBenefitEnrollments(employeeId, isNewEmployee, allFeatureStatus, function() {
                                        succeeded();
                                    },
                                    function() {
                                        failed(getBenefitEnrollFlowUrl(employeeId));
                                    });
                                },
                                function() {
                                    failed(getDocumentUrl(employeeId, isNewEmployee));
                                });
                            },
                            function() {
                                failed(getDirectDepositUrl(employeeId));
                            });
                        },
                        function() {
                            failed(getStateTaxUrl(employeeId));
                        });
                      },
                      function(){
                        failed(getTaxUrl(employeeId, isNewEmployee));
                      });
                    },
                    function(){
                      failed(getEmploymentAuthUrl(employeeId, isNewEmployee));
                    });
                  }, function(){
                    failed(getBasicInfoUrl(employeeId, isNewEmployee));
                  });
                },
                function() {
                    failed();
                }
              );
            },
            function() {
                failed();
            }
          );
        },
        basicInfo: function(employeeId, succeeded, failed){
          validateBasicInfo(employeeId, function(){
            if(succeeded){
              succeeded();
            }
          }, function(){
            if(failed){
              failed();
            }
          });
        }
      }
  }]);
