var brokersControllers = angular.module('benefitmyApp.brokers.controllers',[]);

var clientsController = brokersControllers.controller('clientsController',
  ['$scope', '$location', 'clientListRepository', 'currentUser',
  function clientsController($scope, $location, clientListRepository, currentUser){

    $scope.addClient = function()
    {
      $location.path('/broker/add_client');
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
              employeeCost: benefit.employee_cost_per_period
            });
          array.benefitList.push(sameNameBenefit);
        }
        else
        {
          sameBenefit.options.push({
              optionType:benefit.benefit_option_type,
              totalCost:benefit.total_cost_per_period,
              employeeCost: benefit.employee_cost_per_period
          });
        }
    };
    $scope.backtoDashboard = function(){
      $location.path('/broker');
    }
}]);

var addBenefitController = brokersControllers.controller('addBenefitController', ['$scope', '$location', '$routeParams', 'addBenefitRepository',
  function addBenefitController($scope, $location, $routeParams, addBenefitRepository){
    var clientId = $routeParams.clientId;
    $scope.benefit = {
      benefit_type:"Medical",
      benefit_option_type: "Individual",
      total_cost_per_period: null,
      employee_cost_per_period: null
    };

    $scope.benefit_types = ["Medical", "Dental", "Vision"];
    $scope.benefit_option_types_display = [
      "Individual",
      "Individual plus Spouse",
      "Individual plus Child",
      "Individual plus One",
      "Individual plus children",
      "Family"];

    $scope.addBenefit = function(){
      var viewBenefit = $scope.benefit;
      var apiBenefit = mapBenefit(viewBenefit);
      var request = {company: clientId, benefit: apiBenefit};

      addBenefitRepository.save(request, function(){
        $location.path('/broker/benefits/' + clientId);
      }, function(){
        $scope.saveSucceeded = false;
      });
    }

    var mapBenefit = function(viewBenefit){
      var apiBenefit = {};
      // TODO: Add convertion function to mapp a benefit object from view to a benefit object defined in the API.
      apiBenefit.benefit_type = viewBenefit.benefit_type;
      apiBenefit.total_cost_per_period = viewBenefit.total_cost_per_period;
      apiBenefit.employee_cost_per_period = viewBenefit.employee_cost_per_period;
      apiBenefit.benefit_name = viewBenefit.benefit_name;
      apiBenefit.benefit_option_type = viewBenefit.benefit_option_type.replace(/\s+/g, '_').toLowerCase();

      return apiBenefit;
    }

    $scope.viewBenefits = function(){
      $location.path('/broker/benefits/'+clientId);
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
        
      benefitListRepository.get({clientId:$scope.clientId})
        .$promise.then(function(response){
          $scope.benefit = _.findWhere(response.benefits, {id:$scope.benefitId});
        });
      $scope.benefitDetailArray = [];
      $scope.columnCount = 1;
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
          return valueInput;
      };

      var tryCreateNewPolicyTypeDataSet = function(policyTypeId, policyTypeValue){
        var existingPolicyType = getPolicyTypeObjectById(policyTypeId);
        if(!existingPolicyType){
          //There is no existing policyType, create a new policyType
          var policyType = {policy_type:policyTypeValue, policy_type_id: policyTypeId, policy_array:[]};
          $scope.benefitDetailArray.push(policyType);
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
      };

      var deletePolicyType = function(event){

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
            removeSpan.append('del');
            removeSpan.attr('policy-type-id', policyTypeId);
            removeSpan.on('click', deletePolicyType);
            saveTextContainer.append(removeSpan);
          }
          return saveTextContainer;
      };


      var changeInputKeyPress = function(event){
          if(event.charCode == 13){
            var inputVal = $(event.target).val();
            var optionKey = $(event.target).attr('key');
            var policyTypeId = $(event.target).attr('policy-type-id');
            var targetContainer = $(event.target).parent();
            var showDeleteIcon = false;
            //Populate the data set
            if(targetContainer[0].tagName ==='TH'){
              //This is another new option set.
              if(tryCreateNewPolicyTypeDataSet(policyTypeId, inputVal)){
                updateTableWithNewPolicyType($(event.target), policyTypeId);
              }
              showDeleteIcon = true;
            }
            else if(policyTypeId && optionKey){
              //this is just the option type value
              tryCreateNewPolicyValue(policyTypeId, optionKey, inputVal);
            }
            targetContainer.empty();
            targetContainer.append(createValueDiv(policyTypeId, optionKey, inputVal, showDeleteIcon));

          }
      };

      var lostFocusHandler = function(blurEvent){
        var textInput = $(blurEvent.target);
        var curPolicyTypeId = textInput.attr('policy-type-id');
        var curOptionKey = textInput.attr('key');
        var container = textInput.parent();
        var originalText = textInput.attr('placeholder');
        container.empty();
        container.append(createValueDiv(curPolicyTypeId, curOptionKey, originalText));
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

      $scope.addBenefitDetail = function(){

      };
}]);
