var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('benefitDisplayService',
  ['benefitListRepository',
   'benefitDetailsRepository',
   function(benefitListRepository,
            benefitDetailsRepository){
    return function(companyId, showEmployeePremium, populatedFunc){

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
              pcpLink: benefitOption.benefit_plan.pcp_link,
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


        var convertToDisplayGroup = function(group, medicalArray){


          var optionNameList = [];
          _.each(medicalArray, function(benefit){
            _.each(benefit.benefitOptionArray, function(benefitOption){
              if(!_.contains(optionNameList, benefitOption.name)){
                optionNameList.push(benefitOption.name);
              }
            });
          });


          var policyKeyArray = [];
          _.each(medicalArray, function(benefit){
            _.each(benefit.detailsArray, function(detail){
              var foundKeyItem = _.findWhere(policyKeyArray, {id:detail.benefit_policy_key.id});
              if(!foundKeyItem){
                policyKeyArray.push({id:detail.benefit_policy_key.id, name:detail.benefit_policy_key.name});
              }
            });
          });

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

              group.benefitNameArray.push({id:benefit.benefitId, name:benefit.benefitName, pcpLink: benefit.pcpLink});
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
                var existingPolicyType = _.find(policyTypeArray, function(policyTypeItem){
                  return detailItem.benefit_policy_type.id == policyTypeItem.policyTypeId;
                })
                if(!existingPolicyType){
                  policyTypeArray.push({
                    policyTypeName:detailItem.benefit_policy_type.name, 
                    policyTypeId: detailItem.benefit_policy_type.id});
                }
              });
            }
            else{
              policyTypeArray.push({
                    policyTypeName:'', 
                    policyTypeId: ''});
            }
            sortedPolicyTypeArray = _.sortBy(policyTypeArray, 'policyTypeId');
            if(!group.policyNameArray){
              group.policyNameArray = [];
            }
            _.each(sortedPolicyTypeArray, function(policyType){
              group.policyNameArray.push({colspan:6/policyTypeArray.length, name:policyType.policyTypeName})
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
              _.each(sortedPolicyTypeArray, function(policyType){
                var foundBenefitDetail = _.find(benefit.detailsArray, function(benefitDetailItem){
                  return benefitDetailItem.benefit_policy_type.name === policyType.policyTypeName &&
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
              sameNameBenefit.id = benefit.benefit_plan.id;
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
                    if(benefitOption.benefit_plan.benefit_type.name === 'Medical'){
                      medicalBenefitGroup.groupTitle = benefitOption.benefit_plan.benefit_type.name;
                      populateMedicalArray(medicalArray , benefitOption);
                    }
                    else{
                      insertIntoBenefitArray(nonMedicalBenefitArray, benefitOption);
                    }
                });
                if(medicalArray.length > 0){
                  var sortedMedicalArray = _.sortBy(medicalArray, 'benefitName');
                  _.each(sortedMedicalArray, function(benefit, index){
                    benefitDetailsRepository.query({planId:benefit.benefitId})
                      .$promise.then(function(detailArray){
                        benefit.detailsArray = detailArray;

                        //make sure all the details array elements are all initialized.
                        var unInitDetailsArray = _.find(sortedMedicalArray, function(bt){return !bt.detailsArray});
                        if(!unInitDetailsArray){
                          convertToDisplayGroup(medicalBenefitGroup, sortedMedicalArray);
                          if(populatedFunc){
                            benefitCount = calculateBenefitCount(medicalBenefitGroup, nonMedicalBenefitArray);
                            populatedFunc(medicalBenefitGroup, nonMedicalBenefitArray, benefitCount);
                          }
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
