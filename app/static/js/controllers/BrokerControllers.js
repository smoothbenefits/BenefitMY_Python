'use strict';
var brokersControllers = angular.module('benefitmyApp.brokers.controllers',[]);

var clientsController = brokersControllers.controller('clientsController', [
  '$scope',
  '$state',
  '$stateParams',
  '$location',
  '$modal',
  'clientListRepository',
  'currentUser',
  function clientsController(
    $scope,
    $state,
    $stateParams,
    $location,
    $modal,
    clientListRepository,
    currentUser){

    $scope.addClient = function()
    {
      $location.path('/broker/add_client');
    };

    $scope.viewElegibleBenefits = function(clientId){
      $location.path('/broker/benefits/' + clientId);
    };

    $scope.viewSelectedBenefits = function(clientId){
      $location.path('/broker/benefit/selected/' + clientId);
    };

    $scope.editEmployeeInfo = function(clientId) {
      $state.go('/broker/employee_list', {client_id: clientId});
    };

    var getClientList = function(theUser)
    {
        clientListRepository.get({userId:theUser.id})
        .$promise.then(function(response)
          {
            var clientList =[];
            _.each(response.company_roles, function(company_role)
              {
                if(company_role.company_user_type === 'broker')
                {
                  clientList.push(company_role.company);
                }
              });
            $scope.clientList = clientList;
            $scope.clientCount = _.size(clientList);
          });
    };

    var reloadCurrentState = function() {
        $state.transitionTo($state.current, $stateParams, {
            reload: true,
            inherit: false,
            notify: true
        });
    };

    $scope.editCompanyInfo = function(company) {
        var modalInstance = $modal.open({
            templateUrl: '/static/partials/company_info/modal_edit_company_info.html',
            controller: function($scope, companyId) {
                $scope.companyId = companyId;
                $scope.closeModal = function() {
                    modalInstance.dismiss();
                    reloadCurrentState();
                };
            },
            size: 'lg',
            backdrop: 'static',
            resolve: {
              companyId: function() {
                return company.id;
              }
            }
        });
    };

    currentUser.get()
    .$promise.then(function(response)
         {
            $scope.curUser = response.user;
            getClientList($scope.curUser);
         }
    );
  }]
);

var brokerEmployeeEdit = brokersControllers.controller('brokerEmployeeEdit', [
  '$scope',
  '$state',
  '$stateParams',
  'CompanyEmployeeSummaryService',
  function($scope,
           $state,
           $stateParams,
           CompanyEmployeeSummaryService) {

    var companyId = $stateParams.client_id;
    CompanyEmployeeSummaryService.getCompanyEmployeeSummary(companyId)
    .then(function(companyUsers) {
      $scope.employees = companyUsers;
    });

    $scope.editPersonalInfo = function(employeeId) {
      $state.go('broker_company_employee_personal_info', {employee_id: employeeId});
    };

    $scope.viewEmployeeFamilyMember = function(employeeId) {
      $state.go('broker_view_employee_family', {employeeId: employeeId});
    };

    $scope.back = function() {
      $state.go('/');
    };
  }
]);

var benefitsController = brokersControllers.controller(
   'benefitsController',
   ['$scope',
    '$location',
    '$stateParams',
    '$state',
    '$modal',
    'benefitDisplayService',
    'benefitPlanRepository',
    'BasicLifeInsuranceService',
    'SupplementalLifeInsuranceService',
    'StdService',
    'LtdService',
    'FsaService',
    'HraService',
    'companyRepository',
    function ($scope,
              $location,
              $stateParams,
              $state,
              $modal,
              benefitDisplayService,
              benefitPlanRepository,
              BasicLifeInsuranceService,
              SupplementalLifeInsuranceService,
              StdService,
              LtdService,
              FsaService,
              HraService,
              companyRepository){
      $scope.role = 'Broker';
      $scope.showAddBenefitButton = true;
      $scope.benefitDeletable = true;


      companyRepository.get({clientId: $stateParams.clientId})
      .$promise.then(function(company){
        $scope.company = company;
        benefitDisplayService.getHealthBenefitsForDisplay(company, false)
        .then(function(healthBenefitToDisplay){
          $scope.medicalBenefitGroup = healthBenefitToDisplay.medicalBenefitGroup;
          $scope.nonMedicalBenefitArray = healthBenefitToDisplay.nonMedicalBenefitArray;
          $scope.benefitCount = healthBenefitToDisplay.benefitCount;
        });

        BasicLifeInsuranceService.getLifeInsurancePlansForCompany($scope.company)
        .then(function(response) {
          $scope.lifeInsurancePlans = response;
        });
      });

      $scope.backtoDashboard = function(){
        $location.path('/broker');
      };

      $scope.addBenefitLinkClicked = function(){
        $location.path('/broker/add_benefit/' + $stateParams.clientId);
      };

      $scope.deleteBenefit = function(benefit_id){
        if(benefit_id && confirm('Delete the benefit?')){
          benefitPlanRepository.individual.delete({id:benefit_id}, function(){
            $state.reload();
          });
        }
      };

      $scope.deleteLifeInsurancePlan = function(companyLifeInsurancePlan) {
        BasicLifeInsuranceService.deleteLifeInsurancePlanForCompany(companyLifeInsurancePlan.id, function() {
          $state.reload();
        });
      };

      SupplementalLifeInsuranceService.getPlansForCompany($stateParams.clientId).then(function(response) {
        $scope.supplementalLifeInsurancePlans = response;
      });

      $scope.openSupplementalLifePlanDetailsModal = function(supplementalLifePlan) {
        $scope.detailsModalCompanyPlanToDisplay = supplementalLifePlan;
        $modal.open({
          templateUrl: '/static/partials/benefit_selection/modal_supplemental_life_plan_details.html',
          controller: 'planDetailsModalController',
          size: 'lg',
          scope: $scope
        });
      };

      $scope.deleteSupplementalLifePlan = function(companyPlanToDelete) {
        SupplementalLifeInsuranceService.deleteCompanyPlan(companyPlanToDelete.companyPlanId).then(function() {
          $state.reload();
        });
      };

      StdService.getStdPlansForCompany($stateParams.clientId).then(function(plans) {
        $scope.stdPlans = plans;
      });

      $scope.deleteStdPlan = function(companyStdPlanToDelete) {
        StdService.deleteCompanyStdPlan(companyStdPlanToDelete.companyPlanId).then(function() {
          $state.reload();
        });
      };

      LtdService.getLtdPlansForCompany($stateParams.clientId).then(function(plans) {
        $scope.ltdPlans = plans;
      });

      $scope.deleteLtdPlan = function(companyLtdPlanToDelete) {
        LtdService.deleteCompanyLtdPlan(companyLtdPlanToDelete.companyPlanId).then(function() {
          $state.reload();
        });
      };

      FsaService.getFsaPlanForCompany($stateParams.clientId).then(function(plans) {
        $scope.fsaPlans = plans;
      });

      $scope.deleteFsaPlan = function(companyFsaPlanToDelete) {
        FsaService.deleteCompanyFsaPlan(companyFsaPlanToDelete.companyPlanId).then(function() {
          $state.reload();
        });
      };

      HraService.getPlansForCompany($stateParams.clientId).then(function(response) {
        $scope.hraPlans = response;
      });

      $scope.deleteHraPlan = function(companyPlanToDelete) {
        HraService.deleteCompanyPlan(companyPlanToDelete.companyPlanId).then(function() {
          $state.reload();
        });
      };
}]);

var planDetailsModalController = brokersControllers.controller('planDetailsModalController',
  ['$scope',
   '$modal',
   '$modalInstance',
   function planDetailsModalController(
    $scope,
    $modal,
    $modalInstance){
        $scope.closePlanDetailsModal = function() {
          $modalInstance.dismiss();
        };
}]);

var selectedBenefitsController = brokersControllers.controller('selectedBenefitsController',
  ['$scope',
   '$location',
   '$state',
   '$stateParams',
   '$modal',
   'companyRepository',
   'CompanyEmployeeSummaryService',
   'CompanyBenefitEnrollmentSummaryService',
   'Company1095CService',
  function($scope,
           $location,
           $state,
           $stateParams,
           $modal,
           companyRepository,
           CompanyEmployeeSummaryService,
           CompanyBenefitEnrollmentSummaryService,
           Company1095CService){

      var company_id = $stateParams.client_id;
      $scope.employees = [];

      CompanyBenefitEnrollmentSummaryService.getEnrollmentSummary(company_id)
      .then(function(response){
        $scope.summary = response;
      });

      Company1095CService.get1095CByCompany(company_id).then(function(dataArray){
        $scope.sorted1095CData = dataArray;
      });

      $scope.viewNotStarted = function(){
        $scope.employees = $scope.summary.notStarted;
      };
      $scope.viewNotComplete = function(){
        $scope.employees = $scope.summary.notComplete;
      };
      $scope.viewCompleted = function(){
        $scope.employees = $scope.summary.completed;
      };

      $scope.viewDetails = function(employeeId){
        $state.go('broker_company_employee_enrollment', {company_id:company_id, employee_id:employeeId});
      };

      $scope.back = function(){
        $location.path('/broker');
      };

      $scope.backToDashboard = function(){
        $location.path('/broker');
      };

      $scope.exportCompanyEmployeeSummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryExcelUrl(company_id);
      $scope.exportCompanyEmployeeLifeBeneficiarySummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl(company_id);
      $scope.exportCompanyBenefitsBillingSummaryUrl = CompanyEmployeeSummaryService.getCompanyBenefitsBillingReportExcelUrl(company_id);
      $scope.exportCompanyEmployeeSummaryPdfUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryPdfUrl(company_id);
      $scope.companyHphcExcelUrl = CompanyEmployeeSummaryService.getCompanyHphcExcelUrl(company_id);

      $scope.getEmployee1095cUrl = function(employeeUserId) {
        return CompanyEmployeeSummaryService.getEmployee1095cUrl(employeeUserId);
      };

      $scope.valid1095C = function(){
        return Company1095CService.validate($scope.sorted1095CData);
      };

      $scope.open1095CModal = function(downloadUserId){
        var modalInstance = $modal.open({
          templateUrl: '/static/partials/modal_company_1095_c.html',
          controller: 'company1095CModalController',
          size: 'lg',
          backdrop: 'static',
          resolve: {
              CompanyId: function(){return company_id},
              Existing1095CData: function () {
                  return angular.copy($scope.sorted1095CData);
              }
          }
        });
        modalInstance.result.then(function(saved1095CData){
          $scope.sorted1095CData = saved1095CData;
          if(downloadUserId && Company1095CService.validate($scope.sorted1095CData)){
            window.location = CompanyEmployeeSummaryService.getEmployee1095cUrl(downloadUserId);
          }
        });

      };
}]);

var brokerEmployeeInfoController = brokersControllers.controller('brokerEmployeeInfoController', [
  '$scope',
  '$location',
  '$stateParams',
  function($scope, $location, $stateParams) {
    $scope.employeeId = $stateParams.employee_id;
    $scope.returnTo = $location.path();
  }
]);

var brokerEmployeeEnrollmentController = brokersControllers.controller('brokerEmployeeEnrollmentController', [
  '$scope',
  '$location',
  '$state',
  '$stateParams',
  'companyRepository',
  'peopleRepository',
  'employeeBenefits',
  'FsaService',
  'BasicLifeInsuranceService',
  'SupplementalLifeInsuranceService',
  'CompanyEmployeeSummaryService',
  'StdService',
  'LtdService',
  'HraService',
  function($scope,
           $location,
           $state,
           $stateParams,
           companyRepository,
           peopleRepository,
           employeeBenefits,
           FsaService,
           BasicLifeInsuranceService,
           SupplementalLifeInsuranceService,
           CompanyEmployeeSummaryService,
           StdService,
           LtdService,
           HraService){
    var company_id = $stateParams.company_id;
    $scope.employee = {id:$stateParams.employee_id};

    $scope.backToDashboard = function(){
      $location.path('/broker');
    };

    $scope.back = function(){
      $state.go('broker_benefit_selected', {client_id:company_id});
    };

    companyRepository.get({clientId: company_id})
    .$promise.then(function(response){
        $scope.company = response;

        peopleRepository.ByUser.get({userId:$scope.employee.id})
        .$promise.then(function(employeeDetail){
          $scope.employee.firstName = employeeDetail.first_name;
          $scope.employee.lastName = employeeDetail.last_name;
          $scope.employee.email = employeeDetail.email;
        });

        employeeBenefits.enroll().get({userId:$scope.employee.id, companyId:company_id})
          .$promise.then(function(response){
             $scope.employee.benefits = response.benefits;
             _.each($scope.employee.benefits, function(benefit){
              benefit.updateFormatted = moment(benefit.update_at).format(DATE_FORMAT_STRING);
             });
          });
        employeeBenefits.waive().query({userId:$scope.employee.id, companyId:company_id})
          .$promise.then(function(waivedResponse){
            if(waivedResponse.length > 0){
              $scope.employee.waivedBenefits = waivedResponse;
              _.each($scope.employee.waivedBenefits, function(waived){
                waived.updateFormatted = moment(waived.update_at).format(DATE_FORMAT_STRING);
             });
            }
          });

        // TODO: Could/should FSA information be considered one kind of benefit election
        //       and this logic of getting FSA data for an employee be moved into the
        //       BenefitElectionService?

        FsaService.getFsaElectionForUser($scope.employee.id, company_id).then(function(response) {
          $scope.employee.fsaElection = response;
        });

        // TODO: like the above comment for FSA, Life Insurance, or more generally speaking,
        //       all new benefits going forward, we should consider creating as separate
        //       entity and maybe avoid trying to artificially bundle them together.
        //       Also, once we have tabs working, we should split them into proper flows.
        BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser($scope.employee.id, $scope.company)
        .then(function(response){
          $scope.employee.basicLifeInsurancePlan = response;
        });

        SupplementalLifeInsuranceService.getPlanByUser($scope.employee.id, $scope.company).then(function(plan) {
          $scope.employee.supplementalLifeInsurancePlan = plan;
        });

        // STD
        StdService.getUserEnrolledStdPlanByUser($scope.employee.id, $scope.company.id).then(function(response){
          $scope.employee.userStdPlan = response;
        });

        // LTD
        LtdService.getUserEnrolledLtdPlanByUser($scope.employee.id, $scope.company.id).then(function(response){
          $scope.employee.userLtdPlan = response;
        });

        // HRA
        HraService.getPersonPlanByUser($scope.employee.id, $scope.company.id).then(function(plan) {
          $scope.employee.hraPlan = plan;
        });

    }, function(errorResponse){
      alert(errorResponse.content);
    });
  }
]);


var brokerEmployeeController = brokersControllers.controller('brokerEmployeeController',
  ['$scope',
  '$location',
  '$stateParams',
  'peopleRepository',
  'EmployeeProfileService',
  'CompensationService',
  function brokerEmployeeController(
    $scope,
    $location,
    $stateParams,
    peopleRepository,
    EmployeeProfileService,
    CompensationService){

      var employeeId = $stateParams.employee_id;
      var companyId = $stateParams.cid;
      $scope.employee = {};
      $scope.isBroker = true;

      peopleRepository.ByUser.get({userId:employeeId})
      .$promise.then(function(employeeDetail){
        $scope.employee.first_name = employeeDetail.first_name;
        $scope.employee.last_name = employeeDetail.last_name;
        $scope.employee.email = employeeDetail.email;
        var selfInfo = _.findWhere(employeeDetail.family, {relationship:'self'});
        if(selfInfo){
          $scope.employee.birth_date = selfInfo.birth_date;
          $scope.employee.phones = selfInfo.phones;
          $scope.employee.addresses = selfInfo.addresses;
          $scope.employee.gender = (selfInfo.gender === 'F' ? 'Female' : 'Male');

          // Get the employee profile info that bound to this person
          EmployeeProfileService.getEmployeeProfileForPersonCompany(selfInfo.id, companyId)
          .then(function(profile) {
            $scope.employee.employeeProfile = profile;
            return profile.personId;
          }).then(function(personId) {
            CompensationService.getCompensationByPersonSortedByDate(personId, true)
            .then(function(response) {
              // Return sorted compensation records for the person
              $scope.compensations = response;
            });
          });
        }
      });

      $scope.backToDashboard = function(){
        $location.path('/broker');
      };

      $scope.backToList = function(){
        $location.path('/broker/benefit/selected/' + companyId);
      };
    }]);

var brokerEmployeeFamilyController = brokersControllers.controller(
  'brokerEmployeeFamilyController',
  ['$scope',
   '$state',
   '$stateParams',
  function($scope, $state, $stateParams) {
    $scope.employeeId = $stateParams.employeeId;
    $scope.isOnboarding = false;
  }
]);

var brokerAddBenefits = brokersControllers.controller(
  'brokerAddBenefits',
  ['$scope',
   '$location',
   '$state',
   '$stateParams',
   'tabLayoutGlobalConfig',
  function($scope, $location, $state, $stateParams, tabLayoutGlobalConfig){
    var clientId = $stateParams.clientId;

    $scope.section = _.findWhere(tabLayoutGlobalConfig, {section_name: 'broker_add_benefits'});

    $scope.viewBenefits = function(){
      $location.path('/broker/benefits/' + clientId);
    };

    $scope.goToState = function(state){
      $state.go(state);
    };
  }
]);

var brokerAddBenefitControllerBase = brokersControllers.controller(
  'brokerAddBenefitControllerBase',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'companyRepository',
  function($scope, $state, $stateParams, $controller, companyRepository){
    // Inherite scope from base
    $controller('modalMessageControllerBase', {$scope: $scope});
    $scope.clientId = $stateParams.clientId;
    companyRepository.get({clientId:$scope.clientId})
    .$promise.then(function(company){
      $scope.company = company;
    });
  }]);

var brokerAddBasicLifeInsurance = brokersControllers.controller(
  'brokerAddBasicLifeInsurance',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'currentUser',
   'BasicLifeInsuranceService',
   function($scope,
            $state,
            $stateParams,
            $controller,
            currentUser,
            BasicLifeInsuranceService){

    // Inherite scope from base
    $controller('brokerAddBenefitControllerBase', {$scope: $scope});

    var clientId = $stateParams.clientId;

    $scope.newLifeInsurancePlan = {insurance_type: 'Basic', companyId: clientId};

    var isInteger = function(value) {
      return _.isNumber(value) && value % 1 === 0;
    };

    $scope.isValidMultiplier = function(multiplier) {
      if (!multiplier) {
        // Multiplier is not a required field;
        return true;
      }

      return isInteger(multiplier);
    };

    $scope.buttonEnabled = function() {
      return $scope.newLifeInsurancePlan.name
             && _.isNumber($scope.newLifeInsurancePlan.totalCost)
             && _.isNumber($scope.newLifeInsurancePlan.employeeContribution)
             && (_.isNumber($scope.newLifeInsurancePlan.amount)
                 || _.isNumber($scope.newLifeInsurancePlan.multiplier))
             && $scope.isValidMultiplier($scope.newLifeInsurancePlan.multiplier);
    };

    // Need the user information for the current user (broker)
    $scope.addLifeInsurancePlan = function() {
      currentUser.get().$promise.then(function(response){
        $scope.newLifeInsurancePlan.user = response.user.id;

        // For now, we combine the gestures of
        //  1. Broker creates the plan
        //  2. Broker enrolls the company for the plan
        BasicLifeInsuranceService.saveLifeInsurancePlan($scope.newLifeInsurancePlan)
        .then(function(newPlan) {
          BasicLifeInsuranceService.enrollCompanyForBasicLifeInsurancePlan(newPlan, $scope.newLifeInsurancePlan, $scope.company)
          .then(
            function() {
              var successMessage = "The new basic life insurance plan has been saved successfully."

              $scope.showMessageWithOkayOnly('Success', successMessage);
            },
            function() {
              var failureMessage = "There was a problem saving the data. Please try again."

              $scope.showMessageWithOkayOnly('Failed', failureMessage);
            }
          );
        });
      });
    };
   }
  ]);

var brokerAddSupplementalLifeInsurance = brokersControllers.controller(
  'brokerAddSupplementalLifeInsurance',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'SupplementalLifeInsuranceService',
   'UserService',
   function($scope,
            $state,
            $stateParams,
            $controller,
            SupplementalLifeInsuranceService,
            UserService){

    // Inherite scope from base
    $controller('brokerAddBenefitControllerBase', {$scope: $scope});

    var clientId = $stateParams.clientId;

    SupplementalLifeInsuranceService.getBlankPlanForCompany(clientId).then(function(blankCompanyPlan) {
        $scope.newPlan = blankCompanyPlan;
    });

    // Need the user information for the current user (broker)
    $scope.addPlan = function() {
        SupplementalLifeInsuranceService.addPlanForCompany($scope.newPlan, clientId).then(
            function() {
              var successMessage = "The new supplemental life insurance plan has been saved successfully."

              $scope.showMessageWithOkayOnly('Success', successMessage);
            },
            function() {
              var failureMessage = "There was a problem saving the data. Please make sure all required fields have been filled out and try again."

              $scope.showMessageWithOkayOnly('Failed', failureMessage);
            });
    };
   }
  ]);

var brokerAddStdPlanController = brokersControllers.controller(
  'brokerAddStdPlanController',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'UserService',
   'StdService',
    function($scope,
            $state,
            $stateParams,
            $controller,
            UserService,
            StdService){

        // Inherite scope from base
        $controller('brokerAddBenefitControllerBase', {$scope: $scope});

        $scope.paidByParties = StdService.paidByParties;
        $scope.TRUE = true;
        $scope.FALSE = false;
        $scope.allowUserSelectAmount = false;

        var clientId = $stateParams.clientId;
        $scope.newPlan = {};
        $scope.ageBased = false;
        $scope.toggleAgeBased = function(){
          $scope.ageBased = !$scope.ageBased;
        };

        $scope.newPlan.ageBasedRateTable = StdService.getBlankAgeBasedRateTableViewModel();

        $scope.buttonEnabled = function() {
            return $scope.newPlan.planName && _.isNumber($scope.newPlan.employerContributionPercentage);
        };

        // Need the user information for the current user (broker)
        $scope.saveNewPlan = function() {
            UserService.getCurUserInfo().then(function(userInfo){
                $scope.newPlan.planBroker = userInfo.user.id;
                $scope.newPlan.allowUserSelectAmount = $scope.allowUserSelectAmount;

                StdService.addPlanForCompany($scope.newPlan, clientId).then(
                    function(response) {
                        var successMessage = "The new STD plan has been saved successfully."
                        $scope.showMessageWithOkayOnly('Success', successMessage);
                    },
                    function(response) {
                        var failureMessage = "There was a problem saving the data. Please try again."
                        $scope.showMessageWithOkayOnly('Failed', failureMessage);
                    });
            });
        };
    }
  ]);

var brokerAddLtdPlanController = brokersControllers.controller(
  'brokerAddLtdPlanController',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'UserService',
   'LtdService',
    function($scope,
            $state,
            $stateParams,
            $controller,
            UserService,
            LtdService){

        // Inherite scope from base
        $controller('brokerAddBenefitControllerBase', {$scope: $scope});

        $scope.paidByParties = LtdService.paidByParties;
        $scope.TRUE = true;
        $scope.FALSE = false;
        $scope.allowUserSelectAmount = false;

        var clientId = $stateParams.clientId;
        $scope.newPlan = {};
        $scope.ageBased = false;
        $scope.toggleAgeBased = function(){
          $scope.ageBased = !$scope.ageBased;
        };

        $scope.newPlan.ageBasedRateTable = LtdService.getBlankAgeBasedRateTableViewModel();


        $scope.buttonEnabled = function() {
            return $scope.newPlan.planName && _.isNumber($scope.newPlan.employerContributionPercentage);
        };
        // Need the user information for the current user (broker)
        $scope.saveNewPlan = function() {
            UserService.getCurUserInfo().then(function(userInfo){
                $scope.newPlan.planBroker = userInfo.user.id;
                $scope.newPlan.allowUserSelectAmount = $scope.allowUserSelectAmount;

                LtdService.addPlanForCompany($scope.newPlan, clientId).then(
                    function(response) {
                        var successMessage = "The new LTD plan has been saved successfully."
                        $scope.showMessageWithOkayOnly('Success', successMessage);
                    },
                    function(response) {
                        var failureMessage = "There was a problem saving the data. Please try again."
                        $scope.showMessageWithOkayOnly('Failed', failureMessage);
                    });
            });
        };
    }
  ]);

var brokerAddFsaPlan = brokersControllers.controller(
  'brokerAddFsaPlanController',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'FsaService',
   'UserService',
   function ($scope,
             $state,
             $stateParams,
             $controller,
             FsaService,
             UserService){
    // Inherite scope from base
    $controller('brokerAddBenefitControllerBase', {$scope: $scope});

    var clientId = $stateParams.clientId;
    $scope.newPlan = {};

    $scope.saveNewPlan = function() {
      UserService.getCurUserInfo().then(function(userInfo) {
        var broker = userInfo.user.id;

        FsaService.signUpCompanyForFsaPlan(broker, clientId, $scope.newPlan).then(function(response){
          var successMessage = "The new FSA plan has been saved successfully.";
          $scope.showMessageWithOkayOnly('Success', successMessage);
        });
      }, function(error){
        var failureMessage = "There was a problem saving the data. Please try again.";
        $scope.showMessageWithOkayOnly('Failed', failureMessage);
      });
    };
  }]
);

var brokerAddHraPlanController = brokersControllers.controller(
  'brokerAddHraPlanController',
  ['$scope',
   '$state',
   '$stateParams',
   '$controller',
   'HraService',
   'UserService',
   function($scope,
            $state,
            $stateParams,
            $controller,
            HraService,
            UserService){

    // Inherite scope from base
    $controller('brokerAddBenefitControllerBase', {$scope: $scope});

    var clientId = $stateParams.clientId;

    HraService.getBlankPlanForCompany(clientId).then(function(blankCompanyPlan) {
        $scope.newPlan = blankCompanyPlan;
    });

    // Need the user information for the current user (broker)
    $scope.addPlan = function() {
        HraService.addPlanForCompany($scope.newPlan, clientId).then(
            function() {
              var successMessage = "The new HRA plan has been saved successfully."

              $scope.showMessageWithOkayOnly('Success', successMessage);
            },
            function() {
              var failureMessage = "There was a problem saving the data. Please make sure all required fields have been filled out and try again."

              $scope.showMessageWithOkayOnly('Failed', failureMessage);
        });
    };
   }
]);

var brokerAddHealthBenefits = brokersControllers.controller(
  'brokerAddHealthBenefits',
  ['$scope',
   '$location',
   '$stateParams',
   '$controller',
   'benefitPlanRepository',
   'benefitDetailsRepository',
   'BasicLifeInsuranceService',
   'currentUser',
   'BenefitPolicyKeyService',
   'benefitDisplayService',
    function brokerAddHealthBenefits(
      $scope,
      $location,
      $stateParams,
      $controller,
      benefitPlanRepository,
      benefitDetailsRepository,
      BasicLifeInsuranceService,
      currentUser,
      BenefitPolicyKeyService,
      benefitDisplayService){

      // Inherite scope from base
      $controller('brokerAddBenefitControllerBase', {$scope: $scope});

      var clientId = $stateParams.clientId;

      // Reset/reinitialize the model in scope
      var resetModel = function(selectedBenefitType) {
        if (!selectedBenefitType) {
            selectedBenefitType = '';
        }

        $scope.benefit = {
            mandatory_pcp: false,
            benefit_type: selectedBenefitType,
            benefit_option_types: angular.copy(benefitDisplayService.healthOptionTypes)
          };
      };
      // Initialize the model in scope
      resetModel();

      $scope.isTypeMedical = function(benefitType){
        return benefitType === 'Medical';
      };

      $scope.benefitTypeSelected = function(benefitType){
        return benefitType !== '';
      };

      $scope.benefit_types = ['', 'Medical', 'Dental', 'Vision'];


      $scope.viewBenefits = function(){
        $location.path('/broker/benefits/'+clientId);
      };

      $scope.policyKeyArray = [];

      BenefitPolicyKeyService.getAllKeys().then(function(allKeys) {
        $scope.policyKeyArray = allKeys;
      });

      $scope.benefitDetailArray = [];
      $scope.columnCount = 1;
      $scope.errorString = '';
      var benefitDetailBody = $('#details_container_table_body');

      var getPolicyTypeObjectById = function(policyTypeId){
        return _.findWhere($scope.benefitDetailArray, {policy_type_id: policyTypeId});
      };

      var createInputElement = function(policyTypeId, optionKey, fieldValue, placeHolderText, inputType, showDollar){
          var valueInput = $(document.createElement('input'));
          valueInput.attr('type', inputType);
          valueInput.attr('value', fieldValue);
          valueInput.attr('placeholder', placeHolderText);
          if(optionKey){
            valueInput.attr('key', optionKey);
          }
          if(policyTypeId){
            valueInput.attr('policy-type-id', policyTypeId);
          }
          if(showDollar){
            $scope.noCostError = false;
            valueInput.attr('show-dollar', showDollar);
          }
          valueInput.on('keypress', changeInputKeyPress);
          valueInput.on('blur', lostFocusNoBlankHandler)

          return valueInput;
      };

      var tryCreateNewPolicyTypeDataSet = function(policyTypeId, policyTypeValue){
        var existingPolicyType = getPolicyTypeObjectById(policyTypeId);
        if(!existingPolicyType){
          //There is no existing policyType, create a new policyType
          var policyType = {policy_type:policyTypeValue, policy_type_id: policyTypeId, policy_array:[]};
          $scope.benefitDetailArray.push(policyType);
          $scope.noPolicyTypeError = false;
          $scope.columnCount ++;
          return true;
        }
        else{
          existingPolicyType.policy_type = policyTypeValue;
          return false;
        }
      };

      var updateTableWithNewPolicyType = function(target, policyTypeId){
        var thElement = target.parent();
        var thContainer = thElement.parent();
        var newTh = $(document.createElement('th'));
        //First create the new th on the right hand side
        var newPolicyTypeLinkContainer = $(document.createElement('div'));
        var newPolicyTypeLink = $(document.createElement('a'));
        newPolicyTypeLink.on('click', handleEditElement)
        newPolicyTypeLink.html('Add New Plan');
        newPolicyTypeLinkContainer.addClass('editable-container')
        newPolicyTypeLinkContainer.append(newPolicyTypeLink);
        newTh.append(newPolicyTypeLinkContainer);
        thContainer.append(newTh);

        //update each row with the input
        var tableRows = benefitDetailBody.children('tr');
        _.each(tableRows, function(row){
          var rowKey = $(row).attr('option-key');
          if(rowKey){
            var tableCellArray = $(row).children('td')
            var lastTableCell = tableCellArray[tableCellArray.length -1];
            $(lastTableCell).append(createInputElement(policyTypeId, rowKey, '', 'Add option value', 'text', false));
            $(lastTableCell).attr('policy-type-id', policyTypeId);
            var newTableCell = $(document.createElement('td'));
            $(row).append(newTableCell);
          }
        });
      };


      var tryCreateNewPolicyValue = function(policyTypeId, optionKey, policyValue){
        var policyTypeObject = getPolicyTypeObjectById(policyTypeId);
          var policyPair = _.findWhere(policyTypeObject.policy_array, {policy_key:optionKey});
          if(policyPair){
            policyPair.policy_value = policyValue;
            return false;
          }
          else{
            policyPair = {policy_key:optionKey, policy_value:policyValue};
            policyTypeObject.policy_array.push(policyPair);
            return true;
          }
          $scope.policyKeyNotFound = false;
      };

      var deletePolicyType = function(event){
        //Remove the type from array
        var curPolicyTypeId = $(event.target).attr('policy-type-id');
        var indexToRemove;
        for(var i = 0; i< $scope.benefitDetailArray.length; i++){
          if($scope.benefitDetailArray[i].policy_type_id === curPolicyTypeId){
            indexToRemove = i;
          }
        }
        if(indexToRemove || indexToRemove === 0){
          $scope.benefitDetailArray.splice(indexToRemove, 1);
        }
        //Delete all the td of the tbody.
        var tableRows = benefitDetailBody.children('tr');
        _.each(tableRows, function(row){
          var tableCellArray = $(row).children('td');
          _.each(tableCellArray, function(cell){
            var policyTypeId = $(cell).attr('policy-type-id');
            if(policyTypeId === $(event.target).attr('policy-type-id'))
            {
              $(cell).remove();
            }
          });
        });

        //now delete the th
        var curTh = $(event.target).parent().parent();
        curTh.remove();

      };

      var createValueDiv = function(policyTypeId, optionKey, content, placeHolder, originalType, showDelete, showDollar){
          var saveTextContainer = $(document.createElement('div'));
          saveTextContainer.addClass('editable-container');
          var contentSpan = $(document.createElement('span'));
          if(showDollar){
            saveTextContainer.append('$');
            contentSpan.attr('show-dollar', showDollar);
          }
          if(policyTypeId){
            contentSpan.attr('policy-type-id', policyTypeId);
          }
          if(optionKey){
            contentSpan.attr('key', optionKey);
          }
          if(originalType){
            contentSpan.attr('original-type', originalType);
          }
          if(content){
            contentSpan.append(content);
          }
          else{
            contentSpan.append(placeHolder);
          }
          contentSpan.attr('placeholder', placeHolder);
          contentSpan.on('click', handleEditElement);
          saveTextContainer.append(contentSpan);
          if(showDelete){
            //add delete icon to this div
            var removeSpan = $(document.createElement('a'));
            //removeSpan.append('X');
            removeSpan.attr('policy-type-id', policyTypeId);
            removeSpan.on('click', deletePolicyType);
            removeSpan.attr('href', 'javascript:void(0);')
            removeSpan.addClass('glyphicon glyphicon-remove remove-policy-type');
            saveTextContainer.append(removeSpan);
          }
          return saveTextContainer;
      };

      var updateOptionObject = function(container, input, val){
        $scope.optionEmptyError = false;
        var bOptionName = container.attr('b-option');
        if(bOptionName){
          var optionType = _.findWhere($scope.benefit.benefit_option_types, {name:bOptionName});
          if(optionType){
            var fieldName = container.attr('field-name');
            if(fieldName === 'total'){
              optionType.total_cost_per_period = val;
            }
            else if(fieldName === 'employee'){
              optionType.employee_cost_per_period = val;
            }
          }
        }
      }


      var tryCommitInputValue = function(inputElement){
        $scope.inputUnfilledError = false;
        var inputVal = inputElement.val();
        var optionKey = inputElement.attr('key');
        var policyTypeId = inputElement.attr('policy-type-id');
        var showDollar = inputElement.attr('show-dollar');
        var placeHolder = inputElement.attr('placeholder');
        var originalType = inputElement.attr('type');
        var targetContainer = inputElement.parent();
        if(targetContainer.attr('disabled')){
          return;
        }
        var showDeleteIcon = false;
        //Populate the data set
        if(targetContainer.length > 0 && targetContainer[0].tagName ==='TH'){
          //This is another new option set.
          if(tryCreateNewPolicyTypeDataSet(policyTypeId, inputVal)){
            updateTableWithNewPolicyType(inputElement, policyTypeId);
          }
          showDeleteIcon = true;
        }
        else if(policyTypeId && optionKey){
          //this is just the option type value
          tryCreateNewPolicyValue(policyTypeId, optionKey, inputVal);
        }
        else if(showDollar){
          //Needs a better indicator.
          updateOptionObject(targetContainer, inputElement, inputVal)
        }
        targetContainer.empty();
        targetContainer.append(createValueDiv(policyTypeId, optionKey, inputVal, placeHolder, originalType, showDeleteIcon, showDollar));
      };

      var changeInputKeyPress = function(event){
          if(event.charCode == 13){
            tryCommitInputValue($(event.target));
          }
      };


      function lostFocusNoBlankHandler(blurEvent){
        var inputElement = $(blurEvent.target);
        if(!inputElement.val()){
          return;
        }
        tryCommitInputValue(inputElement);
      }

      function handleEditElement (clickEvent){
        var container = $(clickEvent.target).parent().parent();
        if(container.attr('disabled')){
          return;
        }
        var fieldValue = $(clickEvent.target).html();
        var placeHolderText = $(clickEvent.target).attr('placeholder')
        var curPolicyTypeId = $(clickEvent.target).attr('policy-type-id');
        var showDollar = $(clickEvent.target).attr('show-dollar');
        var originalType = $(clickEvent.target).attr('original-type');
        if(!curPolicyTypeId){
          curPolicyTypeId = $scope.columnCount;
        }
        var curOptionKey = $(clickEvent.target).attr('key');
        var typeTextInput = createInputElement(curPolicyTypeId, curOptionKey, fieldValue, placeHolderText, originalType, showDollar);
        container.empty();
        if(showDollar){
          container.append('$ ');
        }
        container.append(typeTextInput);
        typeTextInput.focus();
      };


      $scope.handleElementEvent = handleEditElement;
      $scope.changeInputKeyPress = changeInputKeyPress;
      $scope.lostFocusNoBlankHandler = lostFocusNoBlankHandler;

      var validateBenefitFields = function(){
        //validate option fields
        var optionTable = $('#plan_option_table');
        var optionTableInputList = optionTable.find('input');
        _.each(optionTableInputList, function(inputElement){
          var optionInput = $(inputElement);
          if(!optionInput.prop('disabled') && !optionInput.val()){
            optionInput.addClass('unfilled-input');
            $scope.optionEmptyError = true;
            return;
          }
        });

        if($scope.optionEmptyError){
          return false;
        }

        if($scope.isTypeMedical($scope.benefit.benefit_type)){
          //first we should validate the table
          var containerTable = $('#details_container_table');
          var inputElements = containerTable.find('input');
          if(inputElements.length > 0)
          {
            _.each(inputElements, function(inputElm){
              var policyValueInput = $(inputElm);
              if(!policyValueInput){
                $(inputElm).addClass('unfilled-input');
                $scope.inputUnfilledError = true;
                return;
              }
              else{
                //save the value into the list.
                var ptid = policyValueInput.attr('policy-type-id');
                var optionKey = policyValueInput.attr('key');
                var policyTypeObject = getPolicyTypeObjectById(ptid);
                var policyPair = _.findWhere(policyTypeObject.policy_array, {policy_key:optionKey});
                if(policyPair){
                  policyPair.policy_value = policyValueInput.val();
                }
              }
            });
          }

          if($scope.inputUnfilledError){
            return false;
          }

          //we validate the benefit object.
          if(!$scope.benefit.benefit_type){
            alert('No benefit type selected!')
            return false;
          }
          var emptyOptionType = _.find($scope.benefit.benefit_option_types, function(optionType){
            return !optionType.disabled && (!optionType.total_cost_per_period || !optionType.employee_cost_per_period);
          });
          if(emptyOptionType){
            $scope.noCostError = true;
            return false;
          }
          else{
            $scope.noCostError = false;
          }

          //now we validate the details array
          if($scope.benefitDetailArray.length <= 0)
          {
            $scope.noPolicyTypeError = true;
            return false;
          }
          _.each($scope.benefitDetailArray, function(benefitTypeContent){
            _.each(benefitTypeContent.policy_array, function(optionPair){
              if(!optionPair.policy_key)
              {
                $scope.policyKeyNotFound = true;
                return;
              }
              if(!optionPair.policy_value)
              {
                optionPair.policy_value = '';
              }
            });
          });
          if($scope.policyKeyNotFound){
            return false;
          }
        }
        return true;
      };

      function saveBenefitOptionPlan(objArray, index, completed, error){
        if(objArray.length <= index){
          //save details
          if(completed){
            completed();
            return;
          }
        }
        benefitPlanRepository.options.save(objArray[index], function(addedBenefit){
          saveBenefitOptionPlan(objArray, index+1, completed, error);
        }, function(errorResponse){
          if(error){
            error(errorResponse);
          }
        });
      };

      function saveToBackendSequential(objArray, index){
        if(objArray.length <= index){
          if($scope.errorString){
            alert($scope.errorString);
          }
          else{
            $location.path('/broker/benefits/' + clientId);
          }
          return;
        }

        benefitDetailsRepository.save({planId:$scope.addedBenefitPlan.id}, objArray[index],
          function(success){
            saveToBackendSequential(objArray, index+1);
          }, function(error){
            $scope.errorString = 'Add Benefit Detail Failed!';
            if(error && error.data){
              $scope.errorString += ' The error is: '+ JSON.stringify(error.data);
            }
            return;
          });
      };

      // Reset the model in scope.
      $scope.resetModel = function(selectedBenefitType) {
        $scope.form.$setPristine()
        resetModel(selectedBenefitType);
      }

      $scope.mandatoryPcpUpdated = function(benefit){
        if(!benefit.mandatory_pcp){
          benefit.pcp_link = undefined;
        }
      }

      $scope.setLink = function(theLink){
        var linkStartRegex = 'http(s)?:(\/)?(\/)?(\w|.)*|ht?t?p?s?:?(\/)?(\/)?';
        var regex = new RegExp(linkStartRegex);
        if(!theLink.match(regex)){
          $scope.benefit.pcp_link = 'http://' + theLink;
        }
      }

      $scope.addBenefit = function(){

        if(!validateBenefitFields()){
          alert('There are errors associated with your data form. The data is not saved. If you do not know what the error is, please refresh the page and try again.');
        }
        else{
          //save to data store
          //first save the new benefit plan
          var new_benefit_plan = {
            benefit_type: $scope.benefit.benefit_type,
            benefit_name: $scope.benefit.benefit_name,
            mandatory_pcp: $scope.benefit.mandatory_pcp,
            pcp_link: $scope.benefit.pcp_link,
          };
          benefitPlanRepository.benefit.save(new_benefit_plan, function(addedBenefitPlan){
            $scope.addedBenefitPlan = addedBenefitPlan.benefit;
            var requestList = [];
            _.each($scope.benefit.benefit_option_types, function(optionTypeItem){
              if(!optionTypeItem.disabled){
                requestList.push({
                  company: clientId,
                  benefit: {
                    benefit_plan_id: $scope.addedBenefitPlan.id,
                    benefit_option_type : optionTypeItem.name.replace(/\s+/g, '_').toLowerCase(),
                    total_cost_per_period: optionTypeItem.total_cost_per_period,
                    employee_cost_per_period: (optionTypeItem.employee_cost_per_period / $scope.company.pay_period_definition.month_factor).toFixed(10)
                  }
                });
              }
            });

          //save the request list to the backend.
            saveBenefitOptionPlan(requestList, 0, function(){
              var apiObjectArray = [];
              _.each($scope.benefitDetailArray, function(benefitTypeContent){
                _.each(benefitTypeContent.policy_array, function(optionPair){
                  var apiObject = {
                      value: optionPair.policy_value,
                      key: optionPair.policy_key,
                      type: benefitTypeContent.policy_type,
                      benefit_plan_id: $scope.addedBenefitPlan.id};
                  apiObjectArray.push(apiObject);
                });
              });

              saveToBackendSequential(apiObjectArray, 0);

              var successMessage = "Your health insurance has been saved. ";
              $scope.showMessageWithOkayOnly('Success', successMessage);
            },
            function(response){
              //Error condition,
              var errorDetail = '';
              if(response && response.data){
                errorDetail = JSON.stringify(response.data);
              }
              alert('Error while saving Benefits! Details: ' + errorDetail);
            });
          });
        }
      };

      $scope.toggleBenefitOptionDisabled = function(option){
        option.disabled = !option.disabled;
        if( _.every($scope.benefit.benefit_option_types, function(option){
            return option.disabled;})){
          alert('The benefit plan must have at least one benefit plan option!');
          option.disabled = !option.disabled;
        }
      };
  }]);

var benefitInputDetailsController = brokersControllers.controller('benefitInputDetailsController',
    ['$scope',
     '$location',
     '$stateParams',
     'benefitListRepository',
     'benefitDetailsRepository',
     function benefitInputDetailsController ($scope,
                                             $location,
                                             $stateParams,
                                             benefitListRepository,
                                             benefitDetailsRepository){
      $scope.clientId = parseInt($stateParams.client_id);
      $scope.benefitId = parseInt($stateParams.benefit_id);

}]);
