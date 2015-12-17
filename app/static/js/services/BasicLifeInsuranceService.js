var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BasicLifeInsuranceService',
  ['BasicLifeInsurancePlanRepository',
   'CompanyBasicLifeInsurancePlanRepository',
   'CompanyUserBasicLifeInsurancePlanRepository',
   'CompanyGroupBasicLifeInsurancePlanRepository',
   'PersonService',
   'CompensationService',
   '$q',
   'EmployeeProfileService',
   'UserService',
  function (
      BasicLifeInsurancePlanRepository,
      CompanyBasicLifeInsurancePlanRepository,
      CompanyUserBasicLifeInsurancePlanRepository,
      CompanyGroupBasicLifeInsurancePlanRepository,
      PersonService,
      CompensationService,
      $q,
      EmployeeProfileService,
      UserService){

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

    var getLifeInsuranceEmployeePremium = function(employeeUserId, basicLifeInsurancePlan) {

      return CompanyUserBasicLifeInsurancePlanRepository.PlanPremiumByUser.get({userId: employeeUserId, planId: basicLifeInsurancePlan.id})
      .$promise;
    };

    var convertNullValueToDash = function(value) {
      if (value) {
        return value;
      } else {
        return '-';
      }
    };

    var mapCreatePlanViewToPlanDomainModel = function(createPlanViewModel) {
        var domainModel = {};

        domainModel.id = createPlanViewModel.planId;
        domainModel.name = createPlanViewModel.name;
        domainModel.user = createPlanViewModel.user;
        domainModel.insurance_type = 'Basic';

        return domainModel;
    };

    var mapCreatePlanViewToCompanyPlanDomainModel = function(createPlanViewModel) {
        var domainModel = {};

        if (createPlanViewModel.amount){
          domainModel.insurance_amount = createPlanViewModel.amount;
        }
        if (createPlanViewModel.multiplier){
          domainModel.salary_multiplier = createPlanViewModel.multiplier;
        }

        domainModel.company = createPlanViewModel.companyId;
        domainModel.life_insurance_plan = createPlanViewModel.planId;

        if (createPlanViewModel.useCostRate) {
            domainModel.total_cost_rate = createPlanViewModel.costRate;
            domainModel.employee_contribution_percentage = createPlanViewModel.employeeContributionPercentage;
        } else {
            domainModel.total_cost_per_period = createPlanViewModel.totalCost;
            domainModel.employee_cost_per_period = (createPlanViewModel.employeeContribution / createPlanViewModel.company.pay_period_definition.month_factor).toFixed(10)
        }

        return domainModel;
    };

    var mapCreatePlanViewToCompanyGroupPlanDomainModel = function(createPlanViewModel) {
        var domainModel = [];

        _.each(createPlanViewModel.selectedCompanyGroups, function(companyGroupModel) {
            domainModel.push({ 
                'company_basic_life_insurance_plan': createPlanViewModel.companyPlanId,
                'company_group': companyGroupModel.id 
            });
        }); 

        return domainModel;
    };

    var saveBasicLifeInsurancePlan = function(planDomainModel) {
        var deferred = $q.defer();

        if(!planDomainModel.id) {
          // Not existing yet, POST it
          BasicLifeInsurancePlanRepository.ById.save({id:planDomainModel.user}, planDomainModel
            , function (successResponse) {
                deferred.resolve(successResponse);
              }
            , function(errorResponse) {
                deferred.reject(errorResponse);
          });
        }
        else {
          // Existing, PUT it
          BasicLifeInsurancePlanRepository.ById.update({id:planDomainModel.id}, planDomainModel
            , function (successResponse) {
                deferred.resolve(successResponse);
              }
            , function(errorResponse) {
                deferred.resolve(errorResponse);
          });
        }
        return deferred.promise;
    };

    var linkBasicLifeInsurancePlanToCompany = function(companyPlanDomainModel) {
        var deferred = $q.defer();

        CompanyBasicLifeInsurancePlanRepository.ById.save({id:companyPlanDomainModel.company}, companyPlanDomainModel
          , function (successResponse) {
              deferred.resolve(successResponse);
            }
          , function(errorResponse) {
              deferred.reject(errorResponse);
            }
        );

        return deferred.promise;
    };

    var linkCompanyBasicLifeInsurancePlanToCompanyGroups = function(companyPlanId, companyGroupPlanDomainModel) {
        var deferred = $q.defer();

        CompanyGroupBasicLifeInsurancePlanRepository.ByCompanyPlan.update({companyPlanId:companyPlanId}, companyGroupPlanDomainModel
          , function (successResponse) {
              deferred.resolve(successResponse);
            }
          , function(errorResponse) {
              deferred.reject(errorResponse);
            }
        );

        return deferred.promise;
    };

    var mapCompanyPlanDomainToViewModel = function(company, companyPlanDomainModel) {
        var viewModel = angular.copy(companyPlanDomainModel);

        viewModel.created_date_for_display = moment(viewModel.created_at).format(DATE_FORMAT_STRING);
        viewModel.life_insurance_plan.display_insurance_type = 'Basic and AD&D';

        if (viewModel.employee_cost_per_period){
            viewModel.employee_cost_per_period = (viewModel.employee_cost_per_period * company.pay_period_definition.month_factor).toFixed(2);
        } else {
            viewModel.employee_cost_per_period = convertNullValueToDash(viewModel.employee_cost_per_period);
        }

        if (viewModel.total_cost_rate) {
            viewModel.total_cost_rate = Number(viewModel.total_cost_rate).toFixed(4);
        } else {
            viewModel.total_cost_rate = convertNullValueToDash(viewModel.total_cost_rate);
        }

        viewModel.total_cost_per_period = convertNullValueToDash(viewModel.total_cost_per_period);
        viewModel.employee_contribution_percentage = convertNullValueToDash(viewModel.employee_contribution_percentage);

        return viewModel;
    };

    var getBasicLifeInsurancePlansForCompany = function(company) {
      var deferred = $q.defer();
      CompanyBasicLifeInsurancePlanRepository.ByCompany.query({companyId:company.id})
        .$promise.then(function(plans) {
          var resultPlans = [];
          _.each(plans, function(companyPlan) {
            if (companyPlan.life_insurance_plan.insurance_type.toLowerCase() === 'basic'){
              resultPlans.push(mapCompanyPlanDomainToViewModel(company, companyPlan));
            }
          });
          deferred.resolve(resultPlans);
        },
        function(failedResponse) {
          deferred.reject(failedResponse);
        });
        return deferred.promise;
    };

    var getBasicLifeInsurancePlansForCompanyGroup = function(company, companyGroupId) {
      var deferred = $q.defer();

      CompanyGroupBasicLifeInsurancePlanRepository.ByCompanyGroup.query({companyGroupId:companyGroupId})
        .$promise.then(function(companyGroupPlans) {
          var resultPlans = [];
          _.each(companyGroupPlans, function(companyGroupPlan) {
            var companyPlan = companyGroupPlan.company_basic_life_insurance_plan;
            if (companyPlan.life_insurance_plan.insurance_type.toLowerCase() === 'basic'){
              resultPlans.push(mapCompanyPlanDomainToViewModel(company, companyPlan));
            }
          });
          deferred.resolve(resultPlans);
        },
        function(failedResponse) {
          deferred.reject(failedResponse);
        });

      return deferred.promise;
    };

    var getBasicLifeInsuranceEnrollmentByUser = function(userId, company) {
      var deferred = $q.defer();

      UserService.getUserDataByUserId(userId).then(
        function(userData) {
            getBasicLifeInsurancePlansForCompanyGroup(company, userData.user.company_group_user[0].company_group.id).then(function(plans){
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
        },
        function(errors) {
            deferred.reject(errors);
        }
      )

      return deferred.promise;
    };

    return {

      createBasicLifeInsurancePlan: function(createPlanViewModel) {
        var deferred = $q.defer();

        var planModel = mapCreatePlanViewToPlanDomainModel(createPlanViewModel);
        saveBasicLifeInsurancePlan(planModel).then(
            function(createdPlan) {
                // Record the new plan Id
                createPlanViewModel.planId = createdPlan.id;
                var companyPlanModel = mapCreatePlanViewToCompanyPlanDomainModel(createPlanViewModel);
                linkBasicLifeInsurancePlanToCompany(companyPlanModel).then(
                    function(createdCompanyPlan) {
                        // Record the new company Plan Id
                        createPlanViewModel.companyPlanId = createdCompanyPlan.id;
                        var companyGroupPlanModel = mapCreatePlanViewToCompanyGroupPlanDomainModel(createPlanViewModel);
                        linkCompanyBasicLifeInsurancePlanToCompanyGroups(createdCompanyPlan.id, companyGroupPlanModel).then(
                            function(createdCompanyGroupPlans) {
                                deferred.resolve(createdCompanyGroupPlans);
                            },
                            function(errors) {
                                deferred.reject(errors);
                            }
                        );
                    },
                    function(errors) {
                        deferred.reject(errors);
                    }
                );
            },
            function(errors) {
                deferred.reject(errors);
            }
        );

        return deferred.promise;
      },

      getBasicLifeInsurancePlansForCompany: getBasicLifeInsurancePlansForCompany,

      getBasicLifeInsurancePlansForCompanyGroup: getBasicLifeInsurancePlansForCompanyGroup,

      getLifeInsuranceEmployeePremium: getLifeInsuranceEmployeePremium,

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
