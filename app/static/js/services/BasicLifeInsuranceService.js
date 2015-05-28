var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BasicLifeInsuranceService', 
  ['BasicLifeInsurancePlanRepository',
   'CompanyBasicLifeInsurancePlanRepository',
   'CompanyUserBasicLifeInsurancePlanRepository',
   'PersonService',
   '$q',
   'EmployeeProfileService',
  function (
      BasicLifeInsurancePlanRepository,
      CompanyBasicLifeInsurancePlanRepository,
      CompanyUserBasicLifeInsurancePlanRepository,
      PersonService,
      $q,
      EmployeeProfileService){

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
          BasicLifeInsurancePlanRepository.ById.save({id:planToSave.user}, planToSave
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
          BasicLifeInsurancePlanRepository.ById.update({id:planToSave.id}, planToSave
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
        BasicLifeInsurancePlanRepository.ById.delete({id:planIdToDelete}
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
        CompanyBasicLifeInsurancePlanRepository.ByCompany.query({companyId:companyId})
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

        CompanyBasicLifeInsurancePlanRepository.ByCompany.query({companyId:companyId})
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

      enrollCompanyForBasicLifeInsurancePlan: function(basicLife, companyBasicLife) {
        var deferred = $q.defer();

        var linkToSave = { 
          "company": companyBasicLife.companyId, 
          "life_insurance_plan": basicLife.id, 
          "insurance_amount": companyBasicLife.amount,
          "salary_multiplier": companyBasicLife.multiplier,
          "total_cost_per_period": companyBasicLife.totalCost,
          "employee_cost_per_period": companyBasicLife.employeeContribution
        };

        CompanyBasicLifeInsurancePlanRepository.ById.save({id:linkToSave.company}, linkToSave
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
        CompanyBasicLifeInsurancePlanRepository.ById.delete({id:companyPlanId}
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
        CompanyUserBasicLifeInsurancePlanRepository.ByUser.query({userId:userId})
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
        CompanyUserBasicLifeInsurancePlanRepository.ByUser.query({userId: userId})
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

              //If we have the salary multiplier, we need to figure that out.
              if(planEnrollments.enrolled &&
                 !planEnrollments.company_life_insurance.insurance_amount && 
                 _.isNumber(planEnrollments.company_life_insurance.salary_multiplier)){
                var basicPlanNeedsSalary = planEnrollments;

                EmployeeProfileService.getEmployeeProfileForCompanyUser(basicPlanNeedsSalary.company_life_insurance.company, userId)
                .then(function(profile){
                  if(_.isNumber(profile.annualBaseSalary)){
                    basicPlanNeedsSalary.company_life_insurance.insurance_amount = profile.annualBaseSalary * basicPlanNeedsSalary.company_life_insurance.salary_multiplier;
                  }
                  else{
                    basicPlanNeedsSalary.company_life_insurance.insurance_amount = 'No Salary Information Found'
                  }
                  successCallBack(basicPlanNeedsSalary);
                });
              }
              else{
                successCallBack(planEnrollments);
              }

            }, function(error){
              errorCallBack(error);
            });
      },

      saveBasicLifeInsurancePlanForUser: function(basicLifeToSave, successCallBack, errorCallBack) {
        var userId = basicLifeToSave.currentUserId;
        PersonService.getSelfPersonInfo(userId)
        .then(function(mainPlanPerson){

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
            CompanyUserBasicLifeInsurancePlanRepository.ById.save({id:planToSave.user}, planToSave)
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
            CompanyUserBasicLifeInsurancePlanRepository.ById.update({id:planToSave.id}, planToSave)
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

      deleteBasicLifeInsurancePlanForUser: function(userId, successCallBack, errorCallBack) {
        CompanyUserBasicLifeInsurancePlanRepository.ByUser.query({userId:userId})
          .$promise.then(function(plans){
            _.each(plans, function(plan){
              if (plan.company_life_insurance.life_insurance_plan 
                  && plan.company_life_insurance.life_insurance_plan.insurance_type === 'Basic'){
                CompanyUserBasicLifeInsurancePlanRepository.ById.delete({id: plan.id});
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
