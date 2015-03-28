var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LifeInsuranceService', 
  ['LifeInsurancePlanRepository',
   'CompanyLifeInsurancePlanRepository',
   'CompanyUserLifeInsurancePlanRepository',
   'employeeFamily',
  function (
      LifeInsurancePlanRepository,
      CompanyLifeInsurancePlanRepository,
      CompanyUserLifeInsurancePlanRepository,
      employeeFamily){

    var getFilteredPercentageNumber = function(rawPercent){
        var reg = new RegExp(/^[0-9]+([\.][0-9]+)*/g);
        var matchedArray = reg.exec(rawPercent);
        if(matchedArray){
          var matchedPercentDigit = matchedArray[0];
          var matchedPercentNumber = parseFloat(matchedPercentDigit).toFixed(2);
          if(matchedPercentNumber > 0 && matchedPercentNumber < 100){
            return matchedPercentNumber;
          }
        }
        return rawPercent;
      };
    return {
      saveLifeInsurancePlan: function(planToSave, successCallBack, errorCallBack) {
        if(!planToSave.id) {
          // Not existing yet, POST it
          LifeInsurancePlanRepository.ById.save({id:planToSave.user}, planToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }  
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
        else {
          // Existing, PUT it 
          LifeInsurancePlanRepository.ById.update({id:planToSave.id}, planToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }  
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
      },

      deleteLifeInsurancePlan: function(planIdToDelete, successCallBack, errorCallBack) {
        LifeInsurancePlanRepository.ById.delete({id:planIdToDelete}
          , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }  
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
            });
      },

      getLifeInsurancePlansForCompany: function(companyId, successCallBack, errorCallBack) {
        CompanyLifeInsurancePlanRepository.ByCompany.query({companyId:companyId})
          .$promise.then(function(plans) {
            if (successCallBack) {
              successCallBack(plans);
            }
          },
          function(failedResponse) {
            if(errorCallBack) {
              errorCallBack(failedResponse)
            }
          });
      },

      enrollCompanyForLifeInsurancePlan: function(companyId, planId, amount, successCallBack, errorCallBack) {
        var linkToSave = { "company":companyId, "life_insurance_plan":planId, "insurance_amount": amount };
        CompanyLifeInsurancePlanRepository.ById.save({id:linkToSave.company}, linkToSave
          , function (successResponse) {
              if (successCallBack) {
                successCallBack(successResponse);
              }  
            }
          , function(errorResponse) {
              if (errorCallBack) {
                errorCallBack(errorResponse);
              }
            }
        );
      },

      deleteLifeInsurancePlanForCompany: function(companyPlanId, successCallBack, errorCallBack) {
        CompanyLifeInsurancePlanRepository.ById.delete({id:companyPlanId}
          , function (successResponse) {
              if (successCallBack) {
                successCallBack(successResponse);
              }  
            }
          , function(errorResponse) {
              if (errorCallBack) {
                errorCallBack(errorResponse);
              }
            }
        );
      },

      getInsurancePlanEnrollmentsByUser: function(userId, successCallBack, errorCallBack) {
        CompanyUserLifeInsurancePlanRepository.ByUser.query({userId:userId})
          .$promise.then(
            function (successResponse) {
              if (successCallBack) {
                successCallBack(successResponse);
              }  
            },
            function(errorResponse) {
              if (errorCallBack) {
                errorCallBack(errorResponse);
              }
            }
          );
      },

      getBasicLifeInsuranceEnrollmentByUser: function(userId, successCallBack, errorCallBack) {
        CompanyUserLifeInsurancePlanRepository.ByUser.query({userId: userId})
          .$promise.then(
            function(response){
              planEnrollments = _.find(response, 
                function(plan){ return plan.life_insurance.life_insurance_plan.insurance_type === 'Basic';}
              );

              if (planEnrollments){
                planEnrollments.enrolled = true;
              }
              else{
                planEnrollments = { enrolled: false, life_insurance_beneficiary: [] };
              }

              var firstTier = [];
              var secondTier = [];
              _.each(planEnrollments.life_insurance_beneficiary, function(beneficiary){
                if (beneficiary.tier === '1'){
                  firstTier.push(beneficiary);
                }
                if (beneficiary.tier === '2'){
                  secondTier.push(beneficiary);
                }
              });
              planEnrollments.life_insurance_beneficiary = firstTier;
              planEnrollments.life_insurance_contingent_beneficiary = secondTier;

              successCallBack(planEnrollments);
            }, function(error){
              errorCallBack(error);
            });
      },

      getInsurancePlanEnrollmentsForAllFamilyMembersByUser: function(userId, successCallBack, errorCallBack) {
        var familyMembers = [];
        var planEnrollments = [];
        var familyPlan = {};

        CompanyUserLifeInsurancePlanRepository.ByUser.query({userId:userId})
          .$promise.then(
            function (successResponse) {
              // Filter out basic life insurance enrolled by user
              planEnrollments = _.filter(successResponse, 
                function(plan){ return plan.life_insurance.life_insurance_plan.insurance_type === 'Extended'; }
                );

              employeeFamily.get({userId:userId})
              .$promise.then(function(familyResponse){
                familyMembers = familyResponse.family;

                var mainPlanPerson = _.findWhere(familyMembers, { relationship: 'self' });

                // Plan belongs to the main account holder, the employee
                var mainPlan = _.findWhere(planEnrollments, { person: mainPlanPerson.id });

                if (!mainPlan) {
                  mainPlan = { 
                    user: userId, 
                    person: mainPlanPerson.id, 
                    insurance_amount: 0, 
                    life_insurance: {}, 
                    life_insurance_beneficiary: [],
                    life_insurance_contingent_beneficiary: []
                  };
                }

                // Categorize beneficiary
                var firstTier = [];
                var secondTier = [];
                _.each(mainPlan.life_insurance_beneficiary, function(beneficiary){
                  if (beneficiary.tier === '1'){
                    firstTier.push(beneficiary);
                  }
                  if (beneficiary.tier === '2'){
                    secondTier.push(beneficiary);
                  }
                });
                mainPlan.life_insurance_beneficiary = firstTier;
                mainPlan.life_insurance_contingent_beneficiary = secondTier;

                if (mainPlan.life_insurance_beneficiary.length > 0)
                {
                  mainPlan.beneficiary_full_name = mainPlan.life_insurance_beneficiary[0].first_name + ' ' + mainPlan.life_insurance_beneficiary[0].last_name;
                }

                // If there are family members do not have life insurance record, add them
                // so if the record is saved, they can be automatically added
                _.each(familyMembers, function(familyMember) {
                  var memberPlan = _.findWhere(planEnrollments, { person: familyMember.id });
                  if (!memberPlan) {
                      var newPlan = { 
                        user:userId, 
                        person:familyMember.id, 
                        insurance_amount:0, 
                        life_insurance: mainPlan.life_insurance, 
                        life_insurance_beneficiary:mainPlan.life_insurance_beneficiary,
                        life_insurance_contingent_beneficiary: mainPlan.life_insurance_contingent_beneficiary 
                      };
                      planEnrollments.push(newPlan);
                  }

                  // Find again, now we should always have a match
                  memberPlan = _.findWhere(planEnrollments, { person: familyMember.id });
                  memberPlan.full_name = familyMember.first_name + ' ' + familyMember.last_name; 
                  memberPlan.relationship = familyMember.relationship;
                  memberPlan.insurance_amount = parseFloat(memberPlan.insurance_amount);
                  memberPlan.last_update_date = new Date(mainPlan.updated_at).toDateString();
                });

                familyPlan.memberPlans = planEnrollments;
                familyPlan.mainPlan = mainPlan;

                if (successCallBack) {
                  successCallBack(familyPlan);
                }  
              });
            },
            function(errorResponse) {
              if (errorCallBack) {
                errorCallBack(errorResponse);
              }
            }
          );
      },

      saveBasicLifeInsurancePlanForUser: function(basicLifeToSave, successCallBack, errorCallBack) {
        var userId = basicLifeToSave.currentUserId;
        employeeFamily.get({userId:userId}).$promise.then(function(familyResponse){
          var mainPlanPerson = _.findWhere(familyResponse.family, { relationship: 'self' });

          var planToSave = {
            "id": basicLifeToSave.id,
            "user": userId,
            "person": mainPlanPerson.id,
            "life_insurance": basicLifeToSave.life_insurance_plan.id,
            "life_insurance_beneficiary": [],
            "insurance_amount": basicLifeToSave.insurance_amount
          };

          // Map beneficiary to according tiers
          if (basicLifeToSave.life_insurance_beneficiary){
            _.each(basicLifeToSave.life_insurance_beneficiary, function(beneficiary){
              beneficiary.tier = "1";
              beneficiary.percentage = getFilteredPercentageNumber(beneficiary.percentage);
              planToSave.life_insurance_beneficiary.push(beneficiary);
            });
          }
          
          if (basicLifeToSave.life_insurance_contingent_beneficiary){
            _.each(basicLifeToSave.life_insurance_contingent_beneficiary, function(beneficiary){
              beneficiary.tier = "2";
              beneficiary.percentage = getFilteredPercentageNumber(beneficiary.percentage);
              planToSave.life_insurance_beneficiary.push(beneficiary);
            });
          }

          // Save basic life insurance
          if (!basicLifeToSave.enrolled) {
            CompanyUserLifeInsurancePlanRepository.ById.save({id:planToSave.user}, planToSave)
              .$promise.then(
                function(response){
                  if (successCallBack) {
                    successCallBack(response);
                  }
                }, 
                function(response){
                  errorCallBack(response);
                });
          } else {
            CompanyUserLifeInsurancePlanRepository.ById.update({id:planToSave.id}, planToSave)
              .$promise.then(
                function(response){
                  if (successCallBack) {
                    successCallBack(response);
                  }
                }, 
                function(response){
                  errorCallBack(response);
                });
          }
        }, function(error){
          errorCallBack(error);
        });
      },

      saveFamilyLifeInsurancePlanForUser: function(familyPlanToSave, successCallBack, errorCallBack) {
        var memberPlansToSave = [];
        var mainPlan = familyPlanToSave.mainPlan;

        _.each(familyPlanToSave.memberPlans, function(memberPlan) {
          var memberPlanToSave = {
            "id":memberPlan.id,
            "user":mainPlan.user,
            "life_insurance":familyPlanToSave.selectedCompanyPlan,
            "person":memberPlan.person,
            "life_insurance_beneficiary":[],
            "insurance_amount":parseFloat(memberPlan.insurance_amount)
          };

          if (memberPlanToSave.person === mainPlan.person) {

            // insert beneficiary tier information
            memberPlanToSave.life_insurance_beneficiary = [];
            if (mainPlan.life_insurance_beneficiary){
              _.each(mainPlan.life_insurance_beneficiary, function(beneficiary){
                beneficiary.tier = "1";
                beneficiary.percentage = getFilteredPercentageNumber(beneficiary.percentage);
                memberPlanToSave.life_insurance_beneficiary.push(beneficiary);
              });
            }

            if (mainPlan.life_insurance_contingent_beneficiary){
              _.each(mainPlan.life_insurance_contingent_beneficiary, function(beneficiary){
                beneficiary.tier = "2";
                beneficiary.percentage = getFilteredPercentageNumber(beneficiary.percentage);
                memberPlanToSave.life_insurance_beneficiary.push(beneficiary);
              });
            }
          }

          if (!memberPlanToSave.id) {
            CompanyUserLifeInsurancePlanRepository.ById.save({id:memberPlanToSave.user}, memberPlanToSave)
              .$promise.then(null, function(response){
                errorCallBack(response);
              });
          } else {
            CompanyUserLifeInsurancePlanRepository.ById.update({id:memberPlanToSave.id}, memberPlanToSave)
              .$promise.then(null, function(response){
                errorCallBack(response);
              });
          }
        });
      },

      deleteFamilyLifeInsurancePlanForUser: function(userId, successCallBack, errorCallBack) {
        CompanyUserLifeInsurancePlanRepository.ByUser.query({userId:userId})
          .$promise.then(function(plans) {
            _.each(plans, function(plan) {
              if (plan.life_insurance_plan && plan.life_insurance_plan.insurance_type === 'Extended'){
                CompanyUserLifeInsurancePlanRepository.ById.delete({id:plan.id});
              }
            });

            if (successCallBack) {
              successCallBack();
            }

          }, function(error) {
            if (errorCallBack) {
              errorCallBack(error);
            }
          });
      },

      deleteBasicLifeInsurancePlanForUser: function(userId, successCallBack, errorCallBack) {
        CompanyUserLifeInsurancePlanRepository.ByUser.query({userId:userId})
          .$promise.then(function(plans){
            _.each(plans, function(plan){
              if (plan.life_insurance.life_insurance_plan 
                  && plan.life_insurance.life_insurance_plan.insurance_type === 'Basic'){
                CompanyUserLifeInsurancePlanRepository.ById.delete({id: plan.id});
              }
            });

            if (successCallBack){
              successCallBack();
            }
          }, function(error){
            if (errorCallBack){
              errorCallBack(error);
            }
          });
      }
    }; 
  }
]);
