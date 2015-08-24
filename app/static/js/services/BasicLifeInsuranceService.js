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

    var getInsuranceAmountBasedOnSalary = function(companyId, userId, policyItem){
      var deferred = $q.defer();
      EmployeeProfileService.getEmployeeProfileForCompanyUser(companyId, userId)
      .then(function(profile){
        if(_.isNumber(profile.annualBaseSalary)){
          policyItem.company_life_insurance.insurance_amount = profile.annualBaseSalary * policyItem.company_life_insurance.salary_multiplier;
        }
        else{
          policyItem.company_life_insurance.insurance_amount = 'No Salary Information Found'
        }
        deferred.resolve(policyItem);
      }, function(error){
        deferred.reject(error);
      });
      return deferred.promise;
    };

    var getLifeInsurancePlansForCompany = function(company) {
      var deferred = $q.defer();
      CompanyBasicLifeInsurancePlanRepository.ByCompany.query({companyId:company.id})
        .$promise.then(function(plans) {
          _.each(plans, function(companyPlan) {
            companyPlan.created_date_for_display = moment(companyPlan.created_at).format(DATE_FORMAT_STRING);
            if (companyPlan.life_insurance_plan.insurance_type.toLowerCase() === 'basic'){
              companyPlan.life_insurance_plan.display_insurance_type = 'Basic and AD&D';
              companyPlan.employee_cost_per_period = (companyPlan.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2);
            }
          });
          deferred.resolve(plans);
        },
        function(failedResponse) {
          deferred.reject(failedResponse);
        });
        return deferred.promise;
      }

    var getBasicLifeInsuranceEnrollmentByUser = function(userId, company) {
      var deferred = $q.defer();
      getLifeInsurancePlansForCompany(company).then(function(plans){
        if(!plans || plans.length <=0){
          deferred.resolve(undefined);
        }
        else{
          CompanyUserBasicLifeInsurancePlanRepository.ByUser.query({userId: userId})
          .$promise.then(
            function(response){

              planEnrollments = _.find(response, function(plan){
                return plan.company_life_insurance;
              });

              // Check if user enrolls basic life insurance. If yes, map response to view model
              // If not, return simple object
              if (planEnrollments){
                planEnrollments.selected = true;
                planEnrollments.waived = false;
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
              } else if (response.length > 0) {
                planEnrollments = { selected: true, waived: true, life_insurance_beneficiary: [] };
              } else {
                planEnrollments = { selected: false, waived: false, life_insurance_beneficiary: [] };
              }

              //If we have the salary multiplier, we need to figure that out.
              if(planEnrollments.enrolled &&
                 !planEnrollments.company_life_insurance.insurance_amount &&
                 _.isNumber(planEnrollments.company_life_insurance.salary_multiplier)){

                getInsuranceAmountBasedOnSalary(planEnrollments.company_life_insurance.company, userId, planEnrollments)
                .then(function(enrolledPlan){
                  deferred.resolve(enrolledPlan);
                });
              }
              else{
                deferred.resolve(planEnrollments);
              }

            }, function(error){
              deferred.reject(error);
            });
        }
      });

      return deferred.promise;
    };

    return {
      saveLifeInsurancePlan: function(planToSave){
        var deferred = $q.defer();
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
                deferred.resolve(successResponse);
              }
            , function(errorResponse) {
                deferred.reject(errorResponse);
          });
        }
        else {
          // Existing, PUT it
          BasicLifeInsurancePlanRepository.ById.update({id:planToSave.id}, planToSave
            , function (successResponse) {
                deferred.resolve(successResponse);
              }
            , function(errorResponse) {
                deferred.resolve(errorResponse);
          });
        }
        return deferred.promise;
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

      getLifeInsurancePlansForCompany: getLifeInsurancePlansForCompany,

      getLifeInsurancePlansForCompanyByType: function(company, plan_type) {
        var deferred = $q.defer();

        CompanyBasicLifeInsurancePlanRepository.ByCompany.query({companyId:company.id})
          .$promise.then(function(plans) {
            var resultPlans = [];
            _.each(plans, function(companyPlan) {
              companyPlan.created_date_for_display = moment(companyPlan.created_at).format(DATE_FORMAT_STRING);
              companyPlan.employee_cost_per_period *= company.pay_period_definition.month_factor;
              companyPlan.employee_cost_per_period = companyPlan.employee_cost_per_period.toFixed(2);
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

      enrollCompanyForBasicLifeInsurancePlan: function(basicLife, companyBasicLife, company) {
        var deferred = $q.defer();

        var linkToSave = {
          "company": company.id,
          "life_insurance_plan": basicLife.id,
          "insurance_amount": companyBasicLife.amount,
          "salary_multiplier": companyBasicLife.multiplier,
          "total_cost_per_period": companyBasicLife.totalCost,
          "employee_cost_per_period": (companyBasicLife.employeeContribution / company.pay_period_definition.month_factor).toFixed(10)
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

      getBasicLifeInsuranceEnrollmentByUser: getBasicLifeInsuranceEnrollmentByUser,

      saveBasicLifeInsurancePlanForUser: function(basicLifeToSave, updateReason, successCallBack, errorCallBack) {
        var userId = basicLifeToSave.currentUserId;
        PersonService.getSelfPersonInfo(userId).then(function(mainPlanPerson){

          var planToSave = {
            "id": basicLifeToSave.id,
            "user": userId,
            "person": mainPlanPerson.id,
            "company_life_insurance": basicLifeToSave.companyLifeInsurancePlan.id,
            "life_insurance_beneficiary": [],
            "insurance_amount": basicLifeToSave.insurance_amount,
            "record_reason_note": updateReason.notes,
            "record_reason": updateReason.selectedReason.id
          };

          // Remove company life insurance if people waives basic life
          if (!basicLifeToSave.selected) {
            planToSave.company_life_insurance = null;
          }

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
      }
    };
  }
]);
