var benefitmyService = angular.module('benefitmyService', ['ngResource']);

benefitmyService.factory('currentUser', [
	'$resource',
	function ($resource){
		return $resource('/api/v1/users/current/', {})
	}
]);

benefitmyService.factory('users', [
	'$resource',
	function ($resource){
		return $resource('/api/v1/users/:userId',
			{userId:'@Id'})
	}
]);

benefitmyService.factory('userLogOut', [
     '$resource',
     function($resource){
     	return $resource('/logout/', {})
     }]
);

benefitmyService.factory('clientListRepository',[
    '$resource',
    function($resource){
        return $resource('/api/v1/users/:userId/company_roles/',
            {userId:'@id'})
}]);

benefitmyService.factory('addClientRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies/', {})
    }]);

benefitmyService.factory('companyRepository', [
  '$resource',
  function($resource){
    return $resource('/api/v1/companies/:clientId', {clientId:'@id'})
  }]);

benefitmyService.factory('companySelectedBenefits', [
  '$resource',
  function($resource){
    return $resource('/api/v1/company_users/:companyId/benefits', {companyId: '@id'})
  }]);

benefitmyService.factory('benefitListRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/companies/:clientId/benefits',
            {clientId:'@id'})
    }]);
benefitmyService.factory('benefitDetailsRepository', [
    '$resource',
    function($resource){
      return $resource('/api/v1/benefit_details/plan=:planId/', {planId:'@id'});
    }]);

benefitmyService.factory('addBenefitRepository', [
    '$resource',
    function($resource){
        return $resource('/api/v1/benefits/', {})
    }]);


benefitmyService.factory('employerRepository', ['$resource',
  function($resource){
  	return $resource('/api/v1/companies/', {})
  }
]);

benefitmyService.factory('employeeBenefits', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/benefits?company=:companyId', {userId: 'employee_id', companyId:'@company_id'})
  }]);

benefitmyService.factory('employerWorkerRepository', ['$resource',
  function($resource){
  	return $resource('/api/v1/companies/:companyId/users',
  		{companyId:'@company_id'})
  }
]);
benefitmyService.factory('usersRepository', ['$resource',
  function($resource){
  	return $resource('/api/v1/users/', {});
  }
]);

benefitmyService.factory('employeeFamily', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/family/', {userId:'user_id'});
  }]);

benefitmyService.factory('userDocument', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/documents/', {userId:'@userId'});
  }])

benefitmyService.factory('documentRepository', ['$resource',
  function($resource){
    return {
      byUser: $resource('/api/v1/users/:userId/documents', {userId:'@user_id'}),
      type: $resource('/api/v1/document_types?company=:companyId', {companyId:'@company_id'}),
      create: $resource('/api/v1/documents/', {}),
      getById: $resource('/api/v1/documents/:id', {id:'@document_id'}),
      sign: $resource('/api/v1/documents/:id/signature', {id:'@document_id'})
    };
  }
]);

benefitmyService.factory('templateRepository', ['$resource',
  function($resource){
    return {
      update: $resource('/api/v1/templates/:id', {id: '@id'}, {
        'update': {method:'PUT'}
      }),
      create: $resource('/api/v1/templates/',{}),
      byCompany: $resource('/api/v1/companies/:companyId/templates/', {companyId:'@company_id'}),
      getById: $resource('/api/v1/templates/:id', {id:'@id'})
    };
  }
]);

benefitmyService.factory('employmentAuthRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/employment_authorization/', {userId: '@userId'});
  }]);

benefitmyService.factory('employeeSignature', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/signature/', {userId: '@userId'});
  }]);

benefitmyService.factory('countRepository', ['$resource',
  function($resource){
    return {
      employeeCount: $resource('/api/v1/company_employees_count/:companyId', {companyId: '@companyId'}),
      brokerCount: $resource('/api/v1/company_brokers_count/:companyId', {companyId: '@companyId'}),
      companyCount: $resource('/api/v1/broker_company_count/:brokerId', {brokerId: '@brokerId'})
    }
  }]);

benefitmyService.factory('emailRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/onboard_email', {});
  }]);

benefitmyService.factory('employeeTaxRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/users/:userId/w4/', {userId:'@userId'});
  }
]);
benefitmyService.factory('peopleRepository', ['$resource',
  function($resource){
    return $resource('/api/v1/people/:personId', {personId:'@personId'});
  }
]);
benefitmyService.factory('EmployeeOnboardingValidationService',
                         ['employeeFamily',
                          'currentUser',
                          'employmentAuthRepository',
                          'employeeTaxRepository',
                          'employeeSignature',
                          'peopleRepository',
  function(employeeFamily,
           currentUser,
           employmentAuthRepository,
           employeeTaxRepository,
           employeeSignature,
           peopleRepository){

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
              peopleRepository.delete({personId:self.id});
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
        });
    };

    var validateW4Info = function(employeeId, succeeded, failed){
      employeeTaxRepository.get({userId:employeeId})
        .$promise.then(function(response){
          if(!response || !response.total_points || response.total_points <= 0){
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

    return function(employeeId, succeeded, failed){
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
    };
  }]);
benefitmyService.factory('EmployeeLetterSignatureValidationService',
  ['documentRepository',
  function(documentRepository){
    return function(employeeId, letterType, success, failure){
      documentRepository.byUser.query({userId:employeeId})
        .$promise.then(function(response){
          var letter = _.find(response, function(l){
            return l.document_type.name === letterType;
          });
          if(!letter && success){
            success();
          }
          else if(letter.signature && letter.signature.signature && success){
            success();
          }
          else if(failure){
            failure();
          }
        })
    };
  }]);

benefitmyService.factory('benefitDisplayService',
  ['benefitListRepository', 
   'benefitDetailsRepository',
   function(benefitListRepository, 
            benefitDetailsRepository){
    return function(companyId, isEmployeeView, populatedFunc){

        var populateMedicalArray = function(array, benefitOption){
          var member = _.findWhere(array, {benefitId:benefitOption.benefit_plan.id});
          if(!member){
            var optionArray = [];
            optionArray.push({
              name: benefitOption.benefit_option_type,
              totalCost: benefitOption.total_cost_per_period,
              employeeCost: benefitOption.employee_cost_per_period
            });
            array.push({
              benefitName: benefitOption.benefit_plan.name,
              benefitId: benefitOption.benefit_plan.id,
              benefitOptionArray: optionArray
            });
          }
          else{
            member.benefitOptionArray.push({
              name: benefitOption.benefit_option_type,
              totalCost: benefitOption.total_cost_per_period,
              employeeCost: benefitOption.employee_cost_per_period
            });
          }
        }

        var populateMedicalGroup = function(group, medicalArray, detailsArray){
          //first retrieve the correct benefit from detailsArray
          if(detailsArray.length <= 0){
            return;
          }
          var benefit = _.findWhere(medicalArray, {benefitId:detailsArray[0].benefit_plan.id});
          if(!benefit){
            return;
          }
          //first work on benefitNameArray
          if(!group.benefitNameArray){
            group.benefitNameArray = [];
          }
          if(!group.benefitOptionMetaArray){
            group.benefitOptionMetaArray = [];
          }

          var optionColSpan = 3;
          var optionEmployeeLabel = 'Employee';
          if(isEmployeeView){
            optionColSpan = 6;
            optionEmployeeLabel = '';
          }

          if(!_.contains(group.benefitNameArray, benefit.benefitName)){

            group.benefitNameArray.push({id:benefit.benefitId, name:benefit.benefitName});
            if(!isEmployeeView){
              group.benefitOptionMetaArray.push({id:benefit.benefitId, name:'Total', colspan:optionColSpan});
            }
            group.benefitOptionMetaArray.push({id:benefit.benefitId, name: optionEmployeeLabel, colspan:optionColSpan});
          }
          //benefitOptionValueArray
          if(!group.benefitOptionValueArray){
            group.benefitOptionValueArray = [];
          }
          _.each(benefit.benefitOptionArray, function(benefitOption){
            var optionValueObject = _.findWhere(group.benefitOptionValueArray, {optionName:benefitOption.name});
            if(!optionValueObject){
              optionValueObject = {optionName:benefitOption.name, benefitCostArray:[]};
              group.benefitOptionValueArray.push(optionValueObject);
            }
            if(!isEmployeeView){
              optionValueObject.benefitCostArray.push({colspan:optionColSpan, value:benefitOption.totalCost});
            }
            optionValueObject.benefitCostArray.push({colspan:optionColSpan, value:benefitOption.employeeCost});
          });
          

          //do policyNameArray
          var policyTypeArray = [];
          _.each(detailsArray, function(detail){
            if(!_.contains(policyTypeArray, detail.benefit_policy_type.name)){
              policyTypeArray.push(detail.benefit_policy_type.name);
            }
          });

          if(!group.policyNameArray){
            group.policyNameArray = [];
          }
          _.each(policyTypeArray, function(policyType){
            group.policyNameArray.push({colspan:6/policyTypeArray.length, name:policyType})
          });

          //do policyList
          if(!group.policyList){
            group.policyList = [];
          }
          _.each(medicalArray, function(benefit){
            _.each(detailsArray, function(detail){
              if(detail.benefit_plan.id === benefit.benefitId){
                var policyListMember = _.findWhere(group.policyList, {id:detail.benefit_policy_key.id});
                if(!policyListMember){
                  policyListMember = {id:detail.benefit_policy_key.id, name:detail.benefit_policy_key.name, valueArray:[]};
                  group.policyList.push(policyListMember);
                }
                policyListMember.valueArray.push({colspan:6/policyTypeArray.length, value:detail.value});
              }
            });
          });
          

        };

        var insertIntoBenefitArray = function(companyBenefitsArray, benefit)
        {
            var benefitType = benefit.benefit_plan.benefit_type.name;
            var array = _.findWhere(companyBenefitsArray, {type:benefitType});
            if(!array)
            {
                array = {type:benefitType, benefitList:[]};
                companyBenefitsArray.push(array);
            }

            var benefitName = benefit.benefit_plan.name;
            var sameBenefit = _.findWhere(array.benefitList, {name:benefitName})
            if(!sameBenefit)
            {
              var sameNameBenefit = {};
              sameNameBenefit.name = benefitName;
              sameNameBenefit.options = [];
              sameNameBenefit.options.push({
                  optionType:benefit.benefit_option_type,
                  totalCost:benefit.total_cost_per_period,
                  employeeCost: benefit.employee_cost_per_period,
                  id: benefit.id
                });
              array.benefitList.push(sameNameBenefit);
            }
            else
            {
              sameBenefit.options.push({
                  optionType:benefit.benefit_option_type,
                  totalCost:benefit.total_cost_per_period,
                  employeeCost: benefit.employee_cost_per_period,
                  id: benefit.id
              });
            }
        };

        var calculateBenefitCount = function(medicalGroup, nonMedicalArray){
          var nonMedicalCount = 0;
          _.each(nonMedicalArray, function(benefitTypeItem){
            nonMedicalCount += benefitTypeItem.benefitList.length;
          });

          var medicalCount = 0;
          if(medicalGroup.benefitNameArray){
            medicalCount = medicalGroup.benefitNameArray.length;
          }

          return nonMedicalCount + medicalCount;
        };

        var medicalBenefitGroup = {};
        var nonMedicalBenefitArray = [];
        var medicalArray = [];
        var benefitCount = 0;

        benefitListRepository.get({clientId:companyId})
            .$promise.then(function(response){
                _.each(response.benefits, function(benefitOption){
                    if(benefitOption.benefit_plan.benefit_type.id === 1){
                      medicalBenefitGroup.groupTitle = benefitOption.benefit_plan.benefit_type.name;
                      populateMedicalArray(medicalArray , benefitOption);
                    }
                    else{
                      insertIntoBenefitArray(nonMedicalBenefitArray, benefitOption);
                    }
                });
                if(medicalArray.length > 0){
                  _.each(medicalArray, function(benefit){
                    benefitDetailsRepository.query({planId:benefit.benefitId})
                      .$promise.then(function(detailArray){
                        populateMedicalGroup(medicalBenefitGroup, medicalArray, detailArray);
                        if(populatedFunc){
                          benefitCount = calculateBenefitCount(medicalBenefitGroup, nonMedicalBenefitArray);
                          populatedFunc(medicalBenefitGroup, nonMedicalBenefitArray, benefitCount);
                        }
                      });
                  });
                }
                else if(populatedFunc){
                  populatedFunc(medicalBenefitGroup, nonMedicalBenefitArray, 
                                calculateBenefitCount(medicalBenefitGroup, nonMedicalBenefitArray));
                }
                
            });
    };
}]);

benefitmyService.factory(
  'documentTypeService',
  ['documentRepository',
   function(documentRepository){
    return {
      getDocumentTypeById: function(companyId, documentTypeId, serviceCallBack){
        documentRepository.type.get({companyId:companyId})
          .$promise.then(function(docTypeResponse){
            var docType = _.findWhere(docTypeResponse.document_types, {id:documentTypeId});
            if(serviceCallBack){
              serviceCallBack(docType);
            }
          });
      },
      getDocumentTypes: function(companyId, serviceCallBack){
        documentRepository.type.get({companyId:companyId})
          .$promise.then(function(response){
            if(serviceCallBack){
              serviceCallBack(response.document_types);
            }
          });
      }
    };
  }]);
