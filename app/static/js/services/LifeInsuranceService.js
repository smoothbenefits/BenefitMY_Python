var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LifeInsuranceService', 
  ['LifeInsurancePlanRepository',
   'CompanyLifeInsurancePlanRepository',
   'CompanyUserLifeInsurancePlanRepository',
   'employeeFamily',
   '$q',
  function (
      LifeInsurancePlanRepository,
      CompanyLifeInsurancePlanRepository,
      CompanyUserLifeInsurancePlanRepository,
      employeeFamily,
      $q){

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
        // map to API fields
        if (planToSave.amount){
          planToSave.insurance_amount = planToSave.amount;
        }
        if (planToSave.multiplier){
          planToSave.salary_multiplier = planToSave.multiplier;
        }

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
            _.each(plans, function(companyPlan) {
              companyPlan.created_date_for_display = moment(companyPlan.created_at).format(DATE_FORMAT_STRING);
              if (companyPlan.life_insurance_plan.insurance_type.toLowerCase() === 'basic'){
                companyPlan.life_insurance_plan.display_insurance_type = 'Basic and AD&D';
              }
            });
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

      getLifeInsurancePlansForCompanyByType: function(companyId, plan_type) {
        var deferred = $q.defer();

        CompanyLifeInsurancePlanRepository.ByCompany.query({companyId:companyId})
          .$promise.then(function(plans) {
            var resultPlans = [];
            _.each(plans, function(companyPlan) {
              companyPlan.created_date_for_display = moment(companyPlan.created_at).format(DATE_FORMAT_STRING);
              if (companyPlan.life_insurance_plan.insurance_type === plan_type) {
                resultPlans.push(companyPlan);
              }
            });
            deferred.resolve(resultPlans);
          },
          function(failedResponse) {
            deferred.reject(failedResponse);
          });

        return deferred.promise;
      },

      enrollCompanyForBasicLifeInsurancePlan: function(companyId, planId, amount, multiplier) {
        var deferred = $q.defer();

        var linkToSave = { 
          "company": companyId, 
          "life_insurance_plan": planId, 
          "insurance_amount": amount,
          "salary_multiplier": multiplier
        };
        CompanyLifeInsurancePlanRepository.ById.save({id:linkToSave.company}, linkToSave
          , function (successResponse) {
              deferred.resolve(successResponse); 
            }
          , function(errorResponse) {
              deferred.reject(errorResponse);
            }
        );

        return deferred.promise;
      },

      enrollCompanyForSupplementalLifeInsurancePlan: function(companyId, planId) {
        var deferred = $q.defer();

        var linkToSave = { 
          "company": companyId, 
          "life_insurance_plan": planId
        };
        CompanyLifeInsurancePlanRepository.ById.save({id:linkToSave.company}, linkToSave
          , function (successResponse) {
              deferred.resolve(successResponse);  
            }
          , function(errorResponse) {
              deferred.reject(errorResponse);
            }
        );

        return deferred.promise;
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
                function(plan){ return plan.company_life_insurance.life_insurance_plan.insurance_type === 'Basic';}
              );

              // Check if user enrolls basic life insurance. If yes, map response to view model
              // If not, return simple object
              if (planEnrollments){
                planEnrollments.enrolled = true;
                planEnrollments.last_update_date = moment(planEnrollments.updated_at).format(DATE_FORMAT_STRING);

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
              }
              else{
                planEnrollments = { enrolled: false, life_insurance_beneficiary: [] };
              }

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
                function(plan){ return plan.company_life_insurance.life_insurance_plan.insurance_type === 'Extended'; }
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
                  memberPlan.last_update_date = moment(mainPlan.updated_at).format(DATE_FORMAT_STRING);
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
            "company_life_insurance": basicLifeToSave.life_insurance_plan.id,
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

        var requests = [];

        _.each(familyPlanToSave.memberPlans, function(memberPlan) {
          var memberPlanToSave = {
            "id":memberPlan.id,
            "user":mainPlan.user,
            "company_life_insurance":familyPlanToSave.selectedCompanyPlan,
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

          var deferred = $q.defer();
          requests.push(deferred);

          if (!memberPlanToSave.id) {
            CompanyUserLifeInsurancePlanRepository.ById.save({id:memberPlanToSave.user}, memberPlanToSave)
              .$promise.then(
                function(response) {
                  deferred.resolve(response);
                }, 
                function(response) {
                  deferred.reject(response);
                });
          } else {
            CompanyUserLifeInsurancePlanRepository.ById.update({id:memberPlanToSave.id}, memberPlanToSave)
              .$promise.then(
              function(response) {
                  deferred.resolve(response);
                }, 
                function(response) {
                  deferred.reject(response);
                });
          }
        });

        // Note:
        // This technique, the usage of $q.all, seems very useful, especially
        // where you'd need to collectively wait for a list of async requests
        // to finish. Or could also be a way to flatten chains of promises.
        $q.all(requests).then(
          function(response) {
            if (successCallBack) {
              successCallBack(response);
            }
          },
          function(error) { 
            if (errorCallBack) {
              errorCallBack(error);
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
              if (plan.company_life_insurance.life_insurance_plan 
                  && plan.company_life_insurance.life_insurance_plan.insurance_type === 'Basic'){
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
