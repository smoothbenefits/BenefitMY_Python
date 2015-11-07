var benefitmyService = angular.module('benefitmyService');


benefitmyService.factory('EmployeePreDashboardValidationService',
                         ['$state',
                          'PersonService',
                          'currentUser',
                          'employmentAuthRepository',
                          'employeeTaxRepository',
                          'PersonService',
  function($state,
           PersonService,
           currentUser,
           employmentAuthRepository,
           employeeTaxRepository,
           PersonService){

    var getUrlFromState = function(state, employeeId) {
        return $state.href(state, { employee_id: employeeId }).replace('#', '');
    };

    var getBasicInfoUrl = function(employeeId){
      return getUrlFromState('employee_onboard.basic_info', employeeId);
    };

    var getEmploymentAuthUrl = function(employeeId){
      return getUrlFromState('employee_onboard.employment', employeeId);
    };

    var getTaxUrl = function(employeeId){
      return getUrlFromState('employee_onboard.tax', employeeId);
    };

    var getDocumentUrl = function(employeeId){
      return getUrlFromState('employee_onboard.document', employeeId);
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

    var validateBasicInfo = function(employeeId, succeeded, failed){
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

    var validateEmploymentAuth = function(employeeId, succeeded, failed){
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
    };

    var validateW4Info = function(employeeId, succeeded, failed){
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
    };

    var validateDocuments = function(employeeId, succeeded, failed) {
        failed();
    };

    return {
        onboarding: function(employeeId, succeeded, failed){
          validateBasicInfo(employeeId, function(){
            validateEmploymentAuth(employeeId, function(){
              validateW4Info(employeeId, function(){
                validateDocuments(employeeId, function() {
                    succeeded();
                },
                function() {
                    failed(getDocumentUrl(employeeId));
                });
              },
              function(){
                failed(getTaxUrl(employeeId));
              });
            },
            function(){
              failed(getEmploymentAuthUrl(employeeId));
            });
          }, function(){
            failed(getBasicInfoUrl(employeeId));
          });
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
