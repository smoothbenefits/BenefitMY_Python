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
    '$routeParams',
    '$route',
    'benefitDisplayService',
    'benefitPlanRepository',
    'LifeInsuranceService',
    function benefitController(
     $scope,
     $location,
     $routeParams,
     $route,
     benefitDisplayService,
     benefitPlanRepository,
     LifeInsuranceService){
        $scope.role = 'Broker';
        $scope.showAddBenefitButton = true;
        $scope.benefitDeletable = true;
        benefitDisplayService($routeParams.clientId, false, function(groupObj, nonMedicalArray, benefitCount){
          $scope.medicalBenefitGroup = groupObj;
          $scope.nonMedicalBenefitArray = nonMedicalArray;
          $scope.benefitCount = benefitCount;

          // add numberic index to medical policy array for ordering
          _.each($scope.medicalBenefitGroup.policyList, function(policy){
            var id = parseInt(policy.id.substring(5, 7).replace("_", ""));
            policy.orderingIndex = id;
          });
        });

        $scope.backtoDashboard = function(){
          $location.path('/broker');
        };

        $scope.addBenefitLinkClicked = function(){
          $location.path('/broker/add_benefit/' + $routeParams.clientId);
        };

        $scope.deleteBenefit = function(benefit_id){
          if(benefit_id && confirm('Delete the benefit?')){
            benefitPlanRepository.individual.delete({id:benefit_id}, function(){
              $route.reload();
            });
          }
        };


        /////////////////////////////////////////////////////////////////////
        // Life Insurance
        // TODO: split this off once we have tabs
        /////////////////////////////////////////////////////////////////////
        LifeInsuranceService.getLifeInsurancePlansForCompany($routeParams.clientId, function(response) {
          $scope.lifeInsurancePlans = response;
          _.each($scope.lifeInsurancePlans, function(companyPlan) {
            companyPlan.created_date_for_display = new Date(companyPlan.created_at).toDateString();
          });
        });

        $scope.deleteLifeInsurancePlan = function(companyLifeInsurancePlan) {
          LifeInsuranceService.deleteLifeInsurancePlanForCompany(companyLifeInsurancePlan.id, function() {
            $route.reload();
          });
        };
}]);




var selectedBenefitsController = brokersControllers.controller('selectedBenefitsController',
  ['$scope', 
   '$location', 
   '$routeParams', 
   'companyRepository', 
   'employeeBenefitElectionFactory',
   'FsaService',
   'LifeInsuranceService',
   'CompanyEmployeeSummaryService',
   function selectedBenefitsController(
    $scope, 
    $location, 
    $routeParams, 
    companyRepository, 
    employeeBenefitElectionFactory,
    FsaService,
    LifeInsuranceService,
    CompanyEmployeeSummaryService){

      var clientId = $routeParams.client_id;
      $scope.employeeList = [];


      companyRepository.get({clientId: clientId}).$promise.then(function(response){
        $scope.companyName = response.name;
      });

      var promise = employeeBenefitElectionFactory(clientId);
      promise.then(function(employeeList){
        
        // TODO: Could/should FSA information be considered one kind of benefit election
        //       and this logic of getting FSA data for an employee be moved into the
        //       employeeBenefitElectionFactory? 
        _.each(employeeList, function(employee) {
          FsaService.getFsaElectionForUser(employee.user.id, function(response) {
            employee.fsaElection = response;
          });
        });

        // TODO: like the above comment for FSA, Life Insurance, or more generally speaking,
        //       all new benefits going forward, we should consider creating as separate 
        //       entity and maybe avoid trying to artificially bundle them together. 
        //       Also, once we have tabs working, we should split them into proper flows.
        _.each(employeeList, function(employee) {
          LifeInsuranceService.getInsurancePlanEnrollmentsForAllFamilyMembersByUser(employee.user.id, function(response) {
            employee.familyInsurancePlan = response;
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

}]);

var brokerEmployeeController = brokersControllers.controller('brokerEmployeeController',
  ['$scope', '$location', '$routeParams', 'employeeFamily',
    function brokerEmployeeController($scope, $location, $routeParams, employeeFamily){
      var employeeId = $routeParams.employee_id;
      var companyId = $routeParams.cid;
      $scope.employee = {};
      employeeFamily.get({userId:employeeId}).$promise.then(function(employeeDetail){
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

var addBenefitController = brokersControllers.controller(
  'addBenefitController',
  ['$scope',
   '$location',
   '$routeParams',
   'benefitPlanRepository',
   'benefitDetailsRepository',
   'LifeInsuranceService',
   'currentUser',
    function addBenefitController(
      $scope,
      $location,
      $routeParams,
      benefitPlanRepository,
      benefitDetailsRepository,
      LifeInsuranceService,
      currentUser){

      var clientId = $routeParams.clientId;
      $scope.benefit = {
        benefit_type:'',
        benefit_option_types: [
          {name:'Individual'},
          {name:'Individual plus Spouse'},
          {name:'Individual plus children'},
          {name:'Individual plus Family'}],
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
          if(!optionInput.val()){
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
            return (!optionType.total_cost_per_period || !optionType.employee_cost_per_period);
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
            requestList.push({
              company: clientId,
              benefit: {
                benefit_type: $scope.benefit.benefit_type,
                benefit_name: $scope.benefit.benefit_name,
                benefit_option_type : optionTypeItem.name.replace(/\s+/g, '_').toLowerCase(),
                total_cost_per_period: optionTypeItem.total_cost_per_period,
                employee_cost_per_period: optionTypeItem.employee_cost_per_period
              }
            });
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

      //////////////////////////////////////////////////////////
      //  Life Insurance
      //  TODO: look into separate this out once we have tabs
      //////////////////////////////////////////////////////////

      // Setup a new blank model
      $scope.newLifeInsurancePlan = {insurance_type: 'Basic'};

      // Need the user information for the current user (broker)
      $scope.addLifeInsurancePlan = function() {
        currentUser.get()
        .$promise.then(function(response)
             {
                $scope.newLifeInsurancePlan.user = response.user.id;

                // For now, we combine the gestures of
                //  1. Broker creates the plan
                //  2. Broker enrolls the company for the plan
                LifeInsuranceService.saveLifeInsurancePlan($scope.newLifeInsurancePlan, function(newPlan) {
                  var planId = newPlan.id;
                  var insurance_amount = 0.0;
                  if ($scope.newLifeInsurancePlan.amount){
                    insurance_amount = $scope.newLifeInsurancePlan.amount;
                  }

                  LifeInsuranceService.enrollCompanyForLifeInsurancePlan(clientId, planId, insurance_amount, function() {
                    $location.path('/broker/benefits/' + clientId);
                  });
                });
             }
        );
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
     '$routeParams',
     'benefitListRepository',
     'benefitDetailsRepository',
     function benefitInputDetailsController ($scope,
                                             $location,
                                             $routeParams,
                                             benefitListRepository,
                                             benefitDetailsRepository){
      $scope.clientId = parseInt($routeParams.client_id);
      $scope.benefitId = parseInt($routeParams.benefit_id);

}]);
