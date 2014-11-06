var brokersControllers = angular.module('benefitmyApp.brokers.controllers',[]);

var findViewController = brokersControllers.controller('findViewController', ['$scope', '$location', 'currentUser', 'clientListRepository',
    function findViewController($scope, $location, currentUser, clientListRepository){
      var userRolesContains = function(userType, userRoles)
      {
        var role = _.findWhere(userRoles, {company_user_type:userType});
        return role != null;
      }
      var determineDashboardLocation = function(userRoles)
      {
        var urlParam = window.location.search;
        if(urlParam !== '')
        {
          var paramNameValueList = urlParam.split('=');
          var paramValue = paramNameValueList[1];
          if(userRolesContains(paramValue, userRoles))
          {
            $location.replace().path('/'+paramValue);
          }
        }
        else if(userRoles.length > 0 && !paramValue)
        {
           var firstRole = userRoles[0].company_user_type;
           $location.replace().path('/'+firstRole);
        }
        else
        {
          window.location.replace('/error?role_match=false');
        }
      }

      var userPromise = currentUser.get()
        .$promise.then(function(response)
             {
                return response.user;
             }
        );
      userPromise.then(function(user){
        clientListRepository.get({userId:user.id})
          .$promise.then(function(response){
            determineDashboardLocation(response.company_roles);
          });
      });
    }
]);


var userController = brokersControllers.controller('userController', ['$scope', '$http', 'currentUser','users', 'userLogOut',
	function userController($scope, $http, currentUser, users, userLogOut) {
    currentUser.get()
      .$promise.then(function(response)
           {
              $scope.curUser = response.user;
           }
      );
    $scope.logout = function ()
    {
        userLogOut.delete()
        .$promise.then(
          function(response){
            window.location = '/';
          },
          function(response)
          {
            window.location = '/';
          });
    }
}]);

var clientsController = brokersControllers.controller('clientsController', ['$scope', '$location', 'clientListRepository', 'currentUser',
  function clientsController($scope, $location, clientListRepository, currentUser){

    $scope.addClient = function()
    {
      $location.path('/add_client');
    }

    var getClientList = function(theUser)
    {
        clientListRepository.get({userId:theUser.id})
        .$promise.then(function(response)
          {
            var clientList =[];
            _.each(response.company_roles, function(company_role)
              {
                if(company_role.company_user_type.toLowerCase() === 'broker')
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
  }
  ]);

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
        $location.path('/benefits/' + clientId);
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
      $location.path('/benefits/'+clientId);
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
