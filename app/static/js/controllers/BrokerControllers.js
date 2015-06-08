'use strict';
var brokersControllers = angular.module('benefitmyApp.brokers.controllers',[]);

var clientsController = brokersControllers.controller('clientsController',
  ['$scope', '$location', 'clientListRepository', 'currentUser',
  function clientsController($scope, $location, clientListRepository, currentUser){

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

    currentUser.get()
    .$promise.then(function(response)
         {
            $scope.curUser = response.user;
            getClientList($scope.curUser);
         }
    );
  }]
);

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
              HraService){
      $scope.role = 'Broker';
      $scope.showAddBenefitButton = true;
      $scope.benefitDeletable = true;
      
      benefitDisplayService($stateParams.clientId, false, function(groupObj, nonMedicalArray, benefitCount){
        $scope.medicalBenefitGroup = groupObj;
        $scope.nonMedicalBenefitArray = nonMedicalArray;
        $scope.benefitCount = benefitCount;
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

      $scope.medicalPolicyPredicate = 'orderIndex';

      $scope.sortBy = function(predicate){
        if ($scope.medicalPolicyPredicate === predicate){
          $scope.medicalPolicyReverse = !$scope.medicalPolicyReverse;
        }
        else{
          $scope.medicalPolicyPredicate = predicate;
        }
      };

      BasicLifeInsuranceService.getLifeInsurancePlansForCompany($stateParams.clientId, function(response) {
        $scope.lifeInsurancePlans = response;
      });

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
   function selectedBenefitsController(
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
   '$stateParams', 
   'companyRepository', 
   'employeeBenefitElectionService',
   'FsaService',
   'BasicLifeInsuranceService',
   'SupplementalLifeInsuranceService',
   'CompanyEmployeeSummaryService',
   'StdService',
   'LtdService',
   'HraService',
   function selectedBenefitsController(
    $scope, 
    $location, 
    $stateParams, 
    companyRepository, 
    employeeBenefitElectionService,
    FsaService,
    BasicLifeInsuranceService,
    SupplementalLifeInsuranceService,
    CompanyEmployeeSummaryService,
    StdService,
    LtdService,
    HraService){

      var clientId = $stateParams.client_id;
      $scope.employeeList = [];

      $scope.backToDashboard = function(){
        $location.path('/broker');
      };

      companyRepository.get({clientId: clientId}).$promise.then(function(response){
        $scope.companyName = response.name;
      });

      var promise = employeeBenefitElectionService(clientId);
      promise.then(function(employeeList){
        
        // TODO: Could/should FSA information be considered one kind of benefit election
        //       and this logic of getting FSA data for an employee be moved into the
        //       employeeBenefitElectionService? 
        _.each(employeeList, function(employee) {
          FsaService.getFsaElectionForUser(employee.user.id, function(response) {
            employee.fsaElection = response;
          });
        });

        // Supplemental life insurance
        _.each(employeeList, function(employee) {
          SupplementalLifeInsuranceService.getPlanByUser(employee.user.id).then(function(plan) {
            employee.supplementalLifeInsurancePlan = plan;
          });
        });

        // Basic life insurance
        _.each(employeeList, function(employee) {
          BasicLifeInsuranceService.getBasicLifeInsuranceEnrollmentByUser(employee.user.id, function(response){
            employee.basicLifeInsurancePlan = response;
          });
        });

        // STD
        _.each(employeeList, function(employee) {
            StdService.getUserEnrolledStdPlanByUser(employee.user.id).then(function(response){
                employee.userStdPlan = response;
            });
        });

        // LTD
        _.each(employeeList, function(employee) {
            LtdService.getUserEnrolledLtdPlanByUser(employee.user.id).then(function(response){
                employee.userLtdPlan = response;
            });
        });

        // HRA
        _.each(employeeList, function(employee) {
          HraService.getPersonPlanByUser(employee.user.id).then(function(plan) {
            employee.hraPlan = plan;
          });
        });

        $scope.clientCount = _.size(employeeList);
        $scope.employeeList = employeeList;
      }, function(errorResponse){
        alert(errorResponse.content);
      });

      $scope.isLifeInsuranceWaived = function(employeeFamilyLifeInsurancePlan) {
        return (!employeeFamilyLifeInsurancePlan) 
          || (!employeeFamilyLifeInsurancePlan.mainPlan)
          || (!employeeFamilyLifeInsurancePlan.mainPlan.id);
      };

      $scope.viewDetails = function(employeeId){
        $location.path('/broker/employee/' + employeeId).search('cid', clientId);
      };

      $scope.back = function(){
        $location.path('/broker');
      };

      $scope.exportCompanyEmployeeSummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeSummaryExcelUrl(clientId);
      $scope.exportCompanyEmployeeLifeBeneficiarySummaryUrl = CompanyEmployeeSummaryService.getCompanyEmployeeLifeInsuranceBeneficiarySummaryExcelUrl(clientId);
}]);

var brokerEmployeeController = brokersControllers.controller('brokerEmployeeController',
  ['$scope', '$location', '$stateParams', 'peopleRepository',
    function brokerEmployeeController($scope, $location, $stateParams, peopleRepository){
      var employeeId = $stateParams.employee_id;
      var companyId = $stateParams.cid;
      $scope.employee = {};
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
        }
      });

      $scope.backToDashboard = function(){
        $location.path('/broker');
      };

      $scope.backToList = function(){
        $location.path('/broker/benefit/selected/' + companyId);
      };
    }]);

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
    $controller('modalMessageControllerBase', {$scope: $scope});
    
    var clientId = $stateParams.clientId;
    $scope.newLifeInsurancePlan = {insurance_type: 'Basic', companyId: clientId};

    $scope.buttonEnabled = function() {
      return $scope.newLifeInsurancePlan.name 
             && _.isNumber($scope.newLifeInsurancePlan.totalCost)
             && _.isNumber($scope.newLifeInsurancePlan.employeeContribution)
             && (_.isNumber($scope.newLifeInsurancePlan.amount) 
                 || _.isNumber($scope.newLifeInsurancePlan.multiplier));
    };

    // Need the user information for the current user (broker)
    $scope.addLifeInsurancePlan = function() {
      currentUser.get().$promise.then(function(response){
        $scope.newLifeInsurancePlan.user = response.user.id;

        // For now, we combine the gestures of
        //  1. Broker creates the plan
        //  2. Broker enrolls the company for the plan
        BasicLifeInsuranceService.saveLifeInsurancePlan($scope.newLifeInsurancePlan, function(newPlan) {

          BasicLifeInsuranceService.enrollCompanyForBasicLifeInsurancePlan(newPlan, $scope.newLifeInsurancePlan).then(
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
    $controller('modalMessageControllerBase', {$scope: $scope});
    
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
        $controller('modalMessageControllerBase', {$scope: $scope});
        
        $scope.paidByParties = StdService.paidByParties;

        var clientId = $stateParams.clientId;
        $scope.newPlan = {};
        
        $scope.buttonEnabled = function() {
            return $scope.newPlan.planName && _.isNumber($scope.newPlan.employerContributionPercentage);
        };

        // Need the user information for the current user (broker)
        $scope.saveNewPlan = function() {
            UserService.getCurUserInfo().then(function(userInfo){
                $scope.newPlan.planBroker = userInfo.user.id;

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
        $controller('modalMessageControllerBase', {$scope: $scope});
        
        $scope.paidByParties = LtdService.paidByParties;

        var clientId = $stateParams.clientId;
        $scope.newPlan = {};

        $scope.buttonEnabled = function() {
            return $scope.newPlan.planName && _.isNumber($scope.newPlan.employerContributionPercentage);
        };

        // Need the user information for the current user (broker)
        $scope.saveNewPlan = function() {
            UserService.getCurUserInfo().then(function(userInfo){
                $scope.newPlan.planBroker = userInfo.user.id;

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
    $controller('modalMessageControllerBase', {$scope: $scope});
     
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
    $controller('modalMessageControllerBase', {$scope: $scope});
    
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
    function brokerAddHealthBenefits(
      $scope,
      $location,
      $stateParams,
      $controller, 
      benefitPlanRepository,
      benefitDetailsRepository,
      BasicLifeInsuranceService,
      currentUser){

      // Inherite scope from base 
      $controller('modalMessageControllerBase', {$scope: $scope});

      var clientId = $stateParams.clientId;
      $scope.benefit = {
        mandatory_pcp: false, 
        benefit_type:'',
        benefit_option_types: [
          {name:'Individual', disabled: false},
          {name:'Individual plus Spouse', disabled: false},
          {name:'Individual plus One', disabled: false},
          {name:'Individual plus Children', disabled: false},
          {name:'Individual plus Family', disabled: false}],
      };
      $('#benefit_type_select').on('change', function(){
        var optionTypeInputs = $('#plan_option_table').find('input');
        _.each(optionTypeInputs, function(input){
          $(input).on('keypress', changeInputKeyPress);
          $(input).on('blur', lostFocusNoBlankHandler);
        });
      });
      $scope.isTypeMedical = function(benefitType){
        return benefitType === 'Medical';
      };

      $scope.benefitTypeSelected = function(benefitType){
        return benefitType !== '';
      };

      $scope.benefit_types = ['Medical', 'Dental', 'Vision'];


      $scope.viewBenefits = function(){
        $location.path('/broker/benefits/'+clientId);
      };

      $scope.policyKeyArray = [
        {position:0, name:'Individual Deductible'},
        {position:1, name:'Family Deductible'},
        {position:2, name:'Hospital-Inpatient'},
        {position:3, name:'Out-patient Day Surgery'},
        {position:4, name:'MRI/CT/PET Scans'},
        {position:5, name:'Lab work/X-Ray'},
        {position:6, name:'Chiropractic'},
        {position:7, name:'Prescription Drugs-30 days'},
        {position:8, name:'Mail order drugs-90 days'},
        {position:9, name:'Annual Rx out of Pocket Maximum'},
        {position:10, name:'Annual Medical out of Pocket Maximum'},
        {position:11, name:'Primary Care Physician required'}];

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
        benefitPlanRepository.group.save(objArray[index], function(addedBenefit){
          $scope.addedBenefit = addedBenefit;
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

        benefitDetailsRepository.save({planId:$scope.addedBenefit.benefits.benefit_plan.id}, objArray[index],
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

      $scope.addBenefit = function(){

        if(!validateBenefitFields()){
          alert('There are errors associated with your data form. The data is not saved. If you do not know what the error is, please refresh the page and try again.');
        }
        else{
          //save to data store
          var requestList = [];
          _.each($scope.benefit.benefit_option_types, function(optionTypeItem){
            if(!optionTypeItem.disabled){
              requestList.push({
                company: clientId,
                benefit: {
                  benefit_type: $scope.benefit.benefit_type,
                  benefit_name: $scope.benefit.benefit_name,
                  mandatory_pcp: $scope.benefit.mandatory_pcp,
                  pcp_link: $scope.benefit.pcp_link,
                  benefit_option_type : optionTypeItem.name.replace(/\s+/g, '_').toLowerCase(),
                  total_cost_per_period: optionTypeItem.total_cost_per_period,
                  employee_cost_per_period: optionTypeItem.employee_cost_per_period
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
                    benefit_plan_id: $scope.addedBenefit.benefits.benefit_plan.id};
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

var addClientController = brokersControllers.controller('addClientController', ['$scope', '$location', 'addClientRepository',
  function addClientController($scope, $location, addClientRepository){
    $scope.client = {};

    $scope.createClient = function(){
      var viewClient = $scope.client;
      var apiClient = mapToAPIClient(viewClient);
      addClientRepository.save(apiClient, function(){
          $location.path('/clients');
      }, function(){
          $scope.saveSucceeded = false;
      });
    }
    var mapToAPIClient = function(viewClient){
      var apiClient = {};
      apiClient.addresses = [];
      apiClient.contacts = [];
      apiClient.name = viewClient.company.name;
      var apiContact = {};
      apiContact.first_name = viewClient.contact.first_name;
      apiContact.last_name = viewClient.contact.last_name;
      apiContact.email = viewClient.contact.email;
      apiContact.person_type = 'primary_contact';
      apiContact.phones = [];
      var apiContactPhone = {};
      apiContactPhone.phone_type = 'work';
      apiContactPhone.number = viewClient.contact.phone;
      apiContact.phones.push(apiContactPhone);
      apiClient.contacts.push(apiContact);
      var apiAddress = {};
      apiAddress.address_type = 'main';
      apiAddress.street_1 = viewClient.address.street1;
      apiAddress.street_2 = viewClient.address.street2;
      apiAddress.city = viewClient.address.city;
      apiAddress.state = viewClient.address.state;
      apiAddress.zipcode = viewClient.address.zip;
      apiClient.addresses.push(apiAddress);
      return apiClient;
    }
  }
]);

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
