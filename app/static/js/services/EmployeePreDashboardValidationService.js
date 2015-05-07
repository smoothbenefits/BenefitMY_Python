var benefitmyService = angular.module('benefitmyService');


benefitmyService.factory('EmployeePreDashboardValidationService',
                         ['employeeFamily',
                          'currentUser',
                          'employmentAuthRepository',
                          'employeeTaxRepository',
                          'employeeSignature',
                          'PersonInfoService',
  function(employeeFamily,
           currentUser,
           employmentAuthRepository,
           employeeTaxRepository,
           employeeSignature,
           PersonInfoService){

    var getBasicInfoUrl = function(employeeId){
      return '/employee/onboard/index/' + employeeId;
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

    var validateBasicInfo = function(employeeId, succeeded, failed){
      //step one (basic info) validation
      employeeFamily.get({userId:employeeId})
        .$promise.then(function(familyResponse){
          var self = _.findWhere(familyResponse.family, {'relationship':'self'});
          if(self){
            //We need to validate this self
            if(!validatePersonInfo(self)){
            //we should remove the family person.
            //Do we have this API?
              PersonInfoService.deletePerson(self.id);
              failed();
            }
            else{
              succeeded();
            }
          }
          else{
            failed();
          }
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
             (!response.user_defined_points || response.user_defined_points <= 0) && 
             (!response.total_points || response.total_points <= 0)){
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

    var validateEmployeeSignature = function(employeeId, succeeded, failed){
      //step 4 the signature for employee
      employeeSignature.get({userId:employeeId})
        .$promise.then(function(signature){
          if(!signature || !signature.signature || signature.signature===''){
            failed();
          }
          else{
           succeeded();
          }
        });
    };

    return {
        onboarding: function(employeeId, succeeded, failed){
          validateBasicInfo(employeeId, function(){
            validateEmploymentAuth(employeeId, function(){
              validateW4Info(employeeId, function(){
                validateEmployeeSignature(employeeId,function(){
                  succeeded();
                }, function(){
                  failed(getSignatureUrl(employeeId));
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
