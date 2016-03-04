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
           UserOnboardingStepStateService){

    var getUrlFromState = function(state, stateParams) {
        return $state.href(state, stateParams).replace('#', '');
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

    var validateBasicInfo = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed){
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

    var validateEmploymentAuth = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed){
      if (!isNewEmployee 
        || (disabledFeatures && disabledFeatures.I9)) {
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

    var validateW4Info = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed){
      if (!isNewEmployee 
        || (disabledFeatures && disabledFeatures.W4)) {
        // Skip I-9 validation if this is not a new employee
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

    var validateDirectDeposit = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed){
      if (disabledFeatures && disabledFeatures.DirectDeposit) {
        // Skip if the feature is disabled
        succeeded();
      } 
      else {
        UserOnboardingStepStateService.getStateByUserAndStep(
            employeeId,
            UserOnboardingStepStateService.Steps.directDeposit).then(
            function(state) {
                if (state && 
                    (state == UserOnboardingStepStateService.States.skipped
                     || state == UserOnboardingStepStateService.States.completed)) {
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

    var validateDocuments = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed) {
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

    var validateBenefitEnrollments = function(employeeId, isNewEmployee, disabledFeatures, succeeded, failed) {
        UserService.getCurUserInfo().then(
            function(userInfo) {
                var company = userInfo.currentRole.company;

                BenefitSummaryService.getBenefitEnrollmentByUser(employeeId, company.id).then(
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
            },
            function(errors) {
                failed();
            }
        );
    };

    return {
        onboarding: function(employeeId, succeeded, failed){
          var disabledFeaturesPromise = UserService.getCurUserInfo().then(function(userInfo) {
            var company = userInfo.currentRole.company;
            return CompanyFeatureService.getDisabledCompanyFeatureByCompany(company.id);
          });
          disabledFeaturesPromise.then(
            function(disabledFeatures){
              UserService.isCurrentUserNewEmployee().then(
                function(isNewEmployee) {
                  validateBasicInfo(employeeId, isNewEmployee, disabledFeatures, function(){
                    validateEmploymentAuth(employeeId, isNewEmployee, disabledFeatures, function(){
                      validateW4Info(employeeId, isNewEmployee, disabledFeatures, function(){
                        validateDirectDeposit(employeeId, isNewEmployee, disabledFeatures, function(){
                            validateDocuments(employeeId, isNewEmployee, disabledFeatures, function() {
                                validateBenefitEnrollments(employeeId, isNewEmployee, disabledFeatures, function() {
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
