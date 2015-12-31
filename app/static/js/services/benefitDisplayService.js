var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('benefitDisplayService',
  ['$q',
   'benefitListRepository',
   'benefitDetailsRepository',
   'BenefitPolicyKeyService',
   function($q,
            benefitListRepository,
            benefitDetailsRepository,
            BenefitPolicyKeyService){
    var HEALTH_OPTION_TYPES = [{name:'Individual', disabled: false},
        {name:'Individual plus Spouse', disabled: false},
        {name:'Individual plus One', disabled: false},
        {name:'Individual plus Children', disabled: false},
        {name:'Individual plus Family', disabled: false}];

    var populateMedicalArray = function(array, benefitOption, company){
      var member = _.findWhere(array, {benefitId:benefitOption.benefit_plan.id});
      if(!member){
        var optionArray = [];
        optionArray.push({
          name: benefitOption.benefit_option_type,
          totalCost: benefitOption.total_cost_per_period,
          employeeCost: (benefitOption.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2)
        });
        array.push({
          benefitName: benefitOption.benefit_plan.name,
          benefitId: benefitOption.benefit_plan.id,
          companyGroups: benefitOption.company_groups,
          pcpLink: benefitOption.benefit_plan.pcp_link,
          benefitOptionArray: optionArray
        });
      }
      else{
        member.benefitOptionArray.push({
          name: benefitOption.benefit_option_type,
          totalCost: benefitOption.total_cost_per_period,
          employeeCost: (benefitOption.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2)
        });
      }
    };

    var convertToDisplayGroup = function(group, medicalArray, benefitPolicyKeys, showEmployeePremium){
      var optionNameList = [];
      _.each(medicalArray, function(benefit){
        _.each(benefit.benefitOptionArray, function(benefitOption){
          if(!_.contains(optionNameList, benefitOption.name)){
            optionNameList.push(benefitOption.name);
          }
        });
      });


      var policyKeyArray = benefitPolicyKeys;

      _.each(medicalArray, function(benefit){

        if(!group.benefitNameArray){
          group.benefitNameArray = [];
        }
        if(!group.benefitOptionMetaArray){
          group.benefitOptionMetaArray = [];
        }

        var optionColSpan = 3;
        var optionEmployeeLabel = 'Employee\n(per pay period)';
        if(showEmployeePremium){
          optionColSpan = 6;
          optionEmployeeLabel = '';
        }

        if(!_.contains(group.benefitNameArray, benefit.benefitName)){

          group.benefitNameArray.push({
            id:benefit.benefitId, 
            name:benefit.benefitName, 
            pcpLink: benefit.pcpLink,
            companyGroups: benefit.companyGroups
          });

          if(!showEmployeePremium){
            group.benefitOptionMetaArray.push({id:benefit.benefitId, name:'Total\n(per month)', colspan:optionColSpan});
          }
          group.benefitOptionMetaArray.push({id:benefit.benefitId, name: optionEmployeeLabel, colspan:optionColSpan});
        }

        //benefitOptionValueArray
        if(!group.benefitOptionValueArray){
          group.benefitOptionValueArray = [];
        }


        //work on the benefit total and employee costs
        _.each(optionNameList, function(metaName){
          var groupOption = _.findWhere(group.benefitOptionValueArray, {optionName: metaName});
          if(!groupOption){
            groupOption = {optionName:metaName, benefitCostArray:[]};
            group.benefitOptionValueArray.push(groupOption);
          }

          var totalCostValue = 'N/A';
          var employeeCostValue = 'N/A';
          var foundOption = _.findWhere(benefit.benefitOptionArray, {name:metaName});
          if(foundOption){
            totalCostValue = '$' + foundOption.totalCost;
            employeeCostValue = '$' + foundOption.employeeCost;
          }
          if(!showEmployeePremium){
            groupOption.benefitCostArray.push({colspan:optionColSpan, value:totalCostValue});
          }
          groupOption.benefitCostArray.push({colspan:optionColSpan, value:employeeCostValue});
        });

        //now work on the benefit policies
        var policyTypeArray = [];
        if(benefit.detailsArray.length > 0){
          _.each(benefit.detailsArray, function(detailItem){
            if(!_.contains(policyTypeArray, detailItem.benefit_policy_type.name)){
              policyTypeArray.push(detailItem.benefit_policy_type.name);
            }
          });
        }
        else{
          policyTypeArray.push('');
        }

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

        _.each(policyKeyArray, function(policyKeyItem){
          var policyListMember = _.findWhere(group.policyList, {id:policyKeyItem.id});
          if(!policyListMember){
            policyListMember = {id:policyKeyItem.id, name:policyKeyItem.name, valueArray:[]};
            group.policyList.push(policyListMember);
          }
          _.each(policyTypeArray, function(policyType){
            var foundBenefitDetail = _.find(benefit.detailsArray, function(benefitDetailItem){
              return benefitDetailItem.benefit_policy_type.name === policyType &&
                benefitDetailItem.benefit_policy_key.id === policyKeyItem.id;
            });
            if(foundBenefitDetail){
              policyListMember.valueArray.push({colspan:6/policyTypeArray.length, value:foundBenefitDetail.value});
            }else{
              policyListMember.valueArray.push({colspan:6/policyTypeArray.length, value:'N/A'});
            }
          });
        });

      });
    };

    var insertIntoBenefitArray = function(companyBenefitsArray, benefit, company){
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
          sameNameBenefit.id = benefit.benefit_plan.id;
          sameNameBenefit.companyGroups = benefit.company_groups;
          sameNameBenefit.options = [];
          sameNameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: (benefit.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2),
              id: benefit.id
            });
          array.benefitList.push(sameNameBenefit);
        }
        else
        {
          sameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: (benefit.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2),
              id: benefit.id
          });
        }
    };

    var sortBenefitOptions = function(optionsArray){
      var sortedArray = [];
      _.each(HEALTH_OPTION_TYPES, function(typeElement){
        var foundArrayElement = _.findWhere(optionsArray, {name:typeElement.name.toLowerCase().replace(/\s/g, '_')});
        if(foundArrayElement){
          sortedArray.push(foundArrayElement);
        }
      });
      return sortedArray;
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

    var getHealthBenefitsForDisplay = function(company, showEmployeePremium){
        var healthBenefitToDisplay = {
          medicalBenefitGroup:{},
          nonMedicalBenefitArray: [],
          benefitCount: 0
        };
        var medicalArray = [];
        var deferred = $q.defer();

        BenefitPolicyKeyService.getAllKeys().then(function(benefitPolicyKeys) {
            benefitListRepository.get({clientId:company.id})
            .$promise.then(function(response){
                _.each(response.benefits, function(benefitOption){
                    if(benefitOption.benefit_plan.benefit_type.name === 'Medical'){
                      healthBenefitToDisplay.medicalBenefitGroup.groupTitle = benefitOption.benefit_plan.benefit_type.name;
                      populateMedicalArray(medicalArray, benefitOption, company);
                    }
                    else{
                      insertIntoBenefitArray(healthBenefitToDisplay.nonMedicalBenefitArray, benefitOption, company);
                    }
                });
                if(medicalArray.length > 0){
                  var sortedMedicalArray = _.sortBy(medicalArray, 'benefitName');
                  _.each(sortedMedicalArray, function(benefit, index){
                    benefit.benefitOptionArray = sortBenefitOptions(benefit.benefitOptionArray);
                    benefitDetailsRepository.query({planId:benefit.benefitId})
                      .$promise.then(function(detailArray){
                        benefit.detailsArray = detailArray;

                        //make sure all the details array elements are all initialized.
                        var unInitDetailsArray = _.find(sortedMedicalArray, function(bt){return !bt.detailsArray});
                        if(!unInitDetailsArray){
                          convertToDisplayGroup(healthBenefitToDisplay.medicalBenefitGroup, sortedMedicalArray, benefitPolicyKeys, showEmployeePremium);
                          healthBenefitToDisplay.benefitCount = calculateBenefitCount(
                            healthBenefitToDisplay.medicalBenefitGroup, 
                            healthBenefitToDisplay.nonMedicalBenefitArray);
                          deferred.resolve(healthBenefitToDisplay);
                        }
                      });
                  });
                }
                else {
                  healthBenefitToDisplay.benefitCount = calculateBenefitCount(
                    healthBenefitToDisplay.medicalBenefitGroup, 
                    healthBenefitToDisplay.nonMedicalBenefitArray);

                  _.each(healthBenefitToDisplay.nonMedicalBenefitArray, function(benefitTypeArray){
                    _.each(benefitTypeArray, function(benefit){
                      benefit.options = sortBenefitOptions(benefit.options);
                    });
                  });
                  deferred.resolve(healthBenefitToDisplay);
                }
            }, function(error){
              deferred.reject(error);
            });
        }, function(error){
          deferred.reject(error);
        });
      return deferred.promise;
    };
    return {
      getHealthBenefitsForDisplay: getHealthBenefitsForDisplay,
      healthOptionTypes: HEALTH_OPTION_TYPES
  };
}]);
