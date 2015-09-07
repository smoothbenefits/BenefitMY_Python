var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyService',
   ['$q', 'addClientRepository',
   function($q, addClientRepository){

     var convertEin = function(rawEin) {
       return rawEin.substring(0, 2) + '-' + rawEin.substring(2);
     };

      var mapToDomainModel = function(viewModel) {
        var apiClient = {};
        apiClient.addresses = [];
        apiClient.contacts = [];
        apiClient.name = viewModel.company.name;

        // Format EIN for company
        apiClient.ein = convertEin(viewModel.company.ein);

        apiClient.offer_of_coverage_code = viewModel.company.offer_of_coverage_code;
        apiClient.pay_period_definition = viewModel.payPeriod.id;
        var apiContact = {};
        apiContact.first_name = viewModel.contact.first_name;
        apiContact.last_name = viewModel.contact.last_name;
        apiContact.email = viewModel.contact.email;
        apiContact.person_type = 'primary_contact';
        apiContact.phones = [];
        var apiContactPhone = {};
        apiContactPhone.phone_type = 'work';
        apiContactPhone.number = viewModel.contact.phone;
        apiContact.phones.push(apiContactPhone);
        apiClient.contacts.push(apiContact);
        var apiAddress = {};
        apiAddress.address_type = 'main';
        apiAddress.street_1 = viewModel.address.street1;
        apiAddress.street_2 = viewModel.address.street2;
        apiAddress.city = viewModel.address.city;
        apiAddress.state = viewModel.address.state.toUpperCase();
        apiAddress.zipcode = viewModel.address.zip;
        apiClient.addresses.push(apiAddress);
        return apiClient;
      };

      var validateViewModel = function(viewModel) {
        var ein = viewModel.company.ein;
        if (!ein) {
          return { isValid: false, message: "EIN is required." };
        }

        if (ein.length != 9) {
          return { isValid: fasle, message: "EIN should be 9 digits long." };
        }

        return { isValid: true, message: "Passed all validations." };
      };

      var createCompany = function(company) {
        var deferred = $q.defer();
        var validationResult = validateViewModel(company);
        if (!validationResult.isValid) {
          deferred.reject(validationResult.message);
        } else {
          var domainModel = mapToDomainModel(company);
          addClientRepository.save(domainModel).$promise
          .then(function(response) {
            deferred.resolve(response);
          }, function(error) {
            deferred.reject(error);
          });
        }

        return deferred.promise;
      }

      return {
         CreateCompany: createCompany
      };
   }
]);
