var brokersControllers = angular.module('benefitmyApp.brokers.controllers',[]);

var clientsController = brokersControllers.controller('clientsController',
  ['$scope', '$location', 'clientListRepository', 'currentUser',
  function clientsController($scope, $location, clientListRepository, currentUser){

    $scope.addClient = function()
    {
      $location.path('/broker/add_client');
    }

    $scope.viewElegibleBenefits = function(clientId){
      $location.path('/broker/benefits/' + clientId);
    }

    $scope.viewSelectedBenefits = function(clientId){
      $location.path('/broker/benefit/selected/' + clientId);
    }

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

          });
    }

    currentUser.get()
    .$promise.then(function(response)
         {
            $scope.curUser = response.user;
            getClientList($scope.curUser);
         }
    );
  }]
);

var benefitsController = brokersControllers.controller('benefitsController', ['$scope', '$location', '$routeParams', 'benefitListRepository', 'companyRepository',
  function benefitController($scope, $location, $routeParams, benefitListRepository, companyRepository){
    var clientId = $routeParams.clientId;
    $scope.clientId = clientId;

    benefitListRepository.get({clientId:clientId})
        .$promise.then(function(response){
            $scope.companyBenefitsArray = [];
            _.each(response.benefits, function(benefit){
                insertIntoBenefitArray($scope.companyBenefitsArray, benefit);
            });
        });
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
    $scope.backtoDashboard = function(){
      $location.path('/broker');
    };
    $scope.viewDetails = function(benefitData){
      $location.path('/broker/benefit/add_details/' + $scope.clientId + "/" + benefitData.id);
    }
}]);

var addBenefitController = brokersControllers.controller(
  'addBenefitController', 
  ['$scope', 
   '$location', 
   '$routeParams', 
   'addBenefitRepository',
   'benefitDetailsRepository',
    function addBenefitController(
      $scope, 
      $location, 
      $routeParams, 
      addBenefitRepository, 
      benefitDetailsRepository){

      var clientId = $routeParams.clientId;
      $scope.benefit = {
        benefit_type:'',
        benefit_option_types: [
          {name:"Individual"},
          {name:"Individual plus One"},
          {name:"Individual plus children"},
          {name:"Family"}],
      };

      $scope.isTypeMedical = function(benefitType){
        return benefitType === 'Medical';
      };

      $scope.benefitTypeSelected = function(benefitType){
        return benefitType !== '';
      };

      $scope.benefit_types = ["Medical", "Dental", "Vision"];

      $scope.viewBenefits = function(){
        $location.path('/broker/benefits/'+clientId);
      };

      $scope.policyKeyArray = [
        {position:0, name:'Individual Deductables'},
        {position:1, name:'Family Deductables'},
        {position:2, name:'Hospital-Inpatient'},
        {position:3, name:'Out-patient Day Surgery'},
        {position:4, name:'MRI/CT/PET Scans'},
        {position:5, name:'Lab work/X-Ray'},
        {position:6, name:'Chiropractic'},
        {position:7, name:'Prescription Drugs-30 days'},
        {position:8, name:'Mail order drugs-90 days'},
        {position:9, name:'Annual Maximum'},
        {position:10, name:'Primary Care Physician required'}];

      $scope.benefitDetailArray = [];
      $scope.columnCount = 1;
      $scope.errorString = "";
      var benefitDetailBody = $('#details_container_table_body');

      var getPolicyTypeObjectById = function(policyTypeId){
        return _.findWhere($scope.benefitDetailArray, {policy_type_id: policyTypeId});
      };

      var createInputElement = function(policyTypeId, optionKey, placeHolderText){
          var valueInput = $(document.createElement('input'));
          valueInput.attr('type', 'text');
          valueInput.attr('placeholder', placeHolderText);
          valueInput.attr('key', optionKey);
          valueInput.attr('policy-type-id', policyTypeId);
          valueInput.on('keypress', changeInputKeyPress);
          valueInput.on('blur', lostFocusHandler)
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
            $(lastTableCell).append(createInputElement(policyTypeId, rowKey, 'Add option value'));
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

      var createValueDiv = function(policyTypeId, optionKey, content, showDelete){
          var saveTextContainer = $(document.createElement('div'));
          saveTextContainer.addClass('editable-container');
          var contentSpan = $(document.createElement('span'));
          contentSpan.attr('policy-type-id', policyTypeId);
          if(optionKey){
            contentSpan.attr('key', optionKey);
          }
          contentSpan.append(content);
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

      var tryCommitInputValue = function(inputElement){
        $scope.inputUnfilledError = false;
        var inputVal = inputElement.val();
        var optionKey = inputElement.attr('key');
        var policyTypeId = inputElement.attr('policy-type-id');
        var targetContainer = inputElement.parent();
        var showDeleteIcon = false;
        //Populate the data set
        if(targetContainer[0].tagName ==='TH'){
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
        targetContainer.empty();
        targetContainer.append(createValueDiv(policyTypeId, optionKey, inputVal, showDeleteIcon));
      };

      var changeInputKeyPress = function(event){
          if(event.charCode == 13){
            tryCommitInputValue($(event.target));
          }
      };

      function lostFocusHandler(blurEvent){
        var textInput = $(blurEvent.target);
        if(!textInput.val()){
          //if the input is empty, we should not set this element to DIV.
          return;
        }
        tryCommitInputValue(textInput);
      };

      function handleEditElement (clickEvent){
        var container = $(clickEvent.target).parent().parent();
        var placeHolderText = $(clickEvent.target).html();
        var curPolicyTypeId = $(clickEvent.target).attr('policy-type-id');
        if(!curPolicyTypeId){
          curPolicyTypeId = $scope.columnCount;
        }
        var curOptionKey = $(clickEvent.target).attr('key');
        var typeTextInput = createInputElement(curPolicyTypeId, curOptionKey, placeHolderText);
        typeTextInput.on('blur', lostFocusHandler)
        container.empty();
        container.append(typeTextInput);
        typeTextInput.focus();
      };


      $scope.handleElementEvent = handleEditElement;


      function saveToBackendSequential(objArray, index){
        if(objArray.length <= index){
          if($scope.errorString){
            alert($scope.errorString);
          }
          else{
            alert('Add Benefit Details Succeeded! You can click "back" to see the benefits');
          }
          return;
        }

        benefitDetailsRepository.save({planId:$scope.benefitId}, objArray[index],
          function(success){
            saveToBackendSequential(objArray, index+1);
          }, function(error){
            $scope.errorString = "Add Benefit Detail Failed! The error is: "+ error.data.stringify();
            return;
          });
      };


      function saveBenefitOptionPlan(objArray, index, completed, error){
        if(objArray.length <= index){
          //save details
          if(completed){
            completed();
          }
        }
        addBenefitRepository.save(objArray[index], function(addedBenefit){
          saveBenefitOptionPlan(objArray, index++, completed, error);
        }, function(errorResponse){
          if(error){
            error(errorResponse);
          }
        });
      };

      var validateBenefitFields = function(){
        //validate option fields
        var optionTable = $('#plan_option_table');
        var optionTableInputList = optionTable.find('input');
        _.each(optionTableInputList, function(inputElement){
          var optionInput = $(inputElement);
          if(!optionInput.val()){
            optionInput.addClass('unfilled-input');
            $scope.optionEmptyError = true;
            return false;
          }
        });

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
                return false;
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
                return false;
              }
              if(!optionPair.policy_value)
              {
                optionPair.policy_value = "";
              }
            });
          });
        }
        return true;
      };


      $scope.addBenefit = function(){

        if(validateBenefitFields()){
          //save to data store
          var requestList = [];
          _.each($scope.benefit.benefit_option_types, function(optionTypeItem){
            requestList.push({
              company: $scope.clientId,
              benefit: {
                benefit_type: $scope.benefit_type,
                benefit_name: $scope.benefit_name,
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
                    benefit_plan_id: $scope.benefitId};
                apiObjectArray.push(apiObject);
              });
            });

            saveToBackendSequential(apiObjectArray, 0);
          }, 
          function(response){
            //Error condition, 
            alert('Error while saving Benefits! Details: ' + response.data.stringify());
          });
        }
      };
  }]);

var selectedBenefitsController = brokersControllers.controller('selectedBenefitsController',
  ['$scope', '$location', '$routeParams', 'companyRepository', 'companySelectedBenefits',
  function selectedBenefitsController($scope, $location, $routeParams, companyRepository, companySelectedBenefits){
    var clientId = $routeParams.client_id;

    companyRepository.get({clientId: clientId}).$promise.then(function(response){
      $scope.companyName = response.name;
    });

    companySelectedBenefits.get({companyId: clientId}).$promise.then(function(response){
      var selectedBenefits = response.benefits;
      $scope.selectionList = [];

      _.each(selectedBenefits, function(benefit){
        var displayBenefit = { enrolled: [] };

        _.each(benefit.enrolleds, function(enrolled){
          if (enrolled.person.relationship === 'self'){
            displayBenefit.name = enrolled.person.first_name + ' ' + enrolled.person.last_name;
            displayBenefit.email = enrolled.person.email;
          }
          var displayEnrolled = { name: enrolled.person.first_name + ' ' + enrolled.person.last_name, relationship: enrolled.person.relationship};
          displayBenefit.enrolled.push(displayEnrolled);
        })

        displayBenefit.selectedPlanName = benefit.benefit.benefit_plan.name
        displayBenefit.selectedPlanType = benefit.benefit.benefit_option_type;

        $scope.selectionList.push(displayBenefit);
      })
    });

    $scope.back = function(){
      $location.path('/broker');
    }
  }])


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
