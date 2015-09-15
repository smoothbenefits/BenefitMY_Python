var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyService',
   ['$q', 'companyRepository', 'employerWorkerRepository', 'PersonService',
   function($q, companyRepository, employerWorkerRepository, PersonService){

      var convertEinFromRaw = function(rawEin) {
        return rawEin.substring(0, 2) + '-' + rawEin.substring(2);
      };

      var convertEinToRaw = function(ein) {
        if (!ein || ein.indexOf("-") != 2) {
            return ein;
        }
        return ein.substring(0, 2) + ein.substring(3);
      };

      var mapToViewModel = function(domainModel) {
        var viewModel = {};

        viewModel.company = {};
        viewModel.company.id = domainModel.id;
        viewModel.company.name = domainModel.name;
        viewModel.company.ein = convertEinToRaw(domainModel.ein);

        viewModel.payPeriod = domainModel.pay_period_definition;

        if (domainModel.contacts && domainModel.contacts.length > 0) {
            var domainContact = domainModel.contacts[0];

            viewModel.contact = {};
            viewModel.contact.first_name = domainContact.first_name;
            viewModel.contact.last_name = domainContact.last_name;
            viewModel.contact.email = domainContact.email;
            viewModel.contact.person_type = domainContact.person_type;
            viewModel.contact.user_id = domainContact.user;
            viewModel.contact.relationship = domainContact.relationship;

            if (domainContact.phones && domainContact.phones.length > 0) {
                var domainPhone = domainContact.phones[0];

                viewModel.contact.phone = domainPhone.number;
            }
        }

        if (domainModel.addresses && domainModel.addresses.length > 0) {
            var domainAddress = domainModel.addresses[0];

            viewModel.address = {};
            viewModel.address.address_type = domainAddress.address_type;
            viewModel.address.street1 = domainAddress.street_1;
            viewModel.address.street2 = domainAddress.street_2;
            viewModel.address.city = domainAddress.city;
            viewModel.address.state = domainAddress.state;
            viewModel.address.zip = domainAddress.zipcode;
        }

        return viewModel;
      };

      var mapToDomainModel = function(viewModel) {
        var apiClient = {};
        apiClient.id = viewModel.company.id
        apiClient.addresses = [];
        apiClient.contacts = [];
        apiClient.name = viewModel.company.name;

        // Format EIN for company
        apiClient.ein = convertEinFromRaw(viewModel.company.ein);

        apiClient.pay_period_definition = viewModel.payPeriod.id;
        var apiContact = {};
        apiContact.first_name = viewModel.contact.first_name;
        apiContact.last_name = viewModel.contact.last_name;
        apiContact.email = viewModel.contact.email;
        apiContact.person_type = 'primary_contact';
        apiContact.user = viewModel.contact.user_id;
        apiContact.relationship = viewModel.contact.relationship;
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
          return { isValid: false, message: "EIN should be 9 digits long." };
        }

        return { isValid: true, message: "Passed all validations." };
      };

      var getCompanyInfo = function(companyId) {
        var deferred = $q.defer();
        companyRepository.get({clientId:companyId})
          .$promise.then(function(companyInfo){
            var viewModel = mapToViewModel(companyInfo);
            deferred.resolve(viewModel);
          },
          function(error) {
            deferred.reject(error);
          });
        return deferred.promise;
      };

      var saveCompanyInfo = function(company) {
        var deferred = $q.defer();

        var validationResult = validateViewModel(company);
        if (!validationResult.isValid) {
          deferred.reject(validationResult.message);
        } else {
          var domainModel = mapToDomainModel(company);

          if (domainModel.id) {
            companyRepository.update({clientId:domainModel.id}, domainModel).$promise
              .then(function(response) {
                deferred.resolve(response);
              }, function(error) {
                deferred.reject(error);
              });
          } else {
            companyRepository.save(domainModel).$promise
              .then(function(response) {
                deferred.resolve(response);
              }, function(error) {
                deferred.reject(error);
              });
          }
        }

        return deferred.promise;
      };

      // Copied shamelessly from http://jsfiddle.net/ExpertSystem/mg2cU/
      var asyncCall =   function(listOfPromises, onErrorCallback, finalCallback) {

        listOfPromises  = listOfPromises  || [];
        onErrorCallback = onErrorCallback || angular.noop;
        finalCallback   = finalCallback   || angular.noop;

        // Create a new list of promises
        // that can "recover" from rejection
        var newListOfPromises = listOfPromises.map(function (promise) {
          return promise.catch(function (reason) {

            // First call the `onErrroCallback`
            onErrorCallback(reason);

            // Change the returned value to indicate that it was rejected
            // Based on the type of `reason` you might need to change this
            // (e.g. if `reason` is an object, add a `rejected` property)
            return 'rejected: ' + reason;
          });
        });

        // Finally, we create a "collective" promise that calls `finalCallback` when resolved.
        // Thanks to our modifications, it will never get rejected !
        $q.all(newListOfPromises).then(finalCallback);
      };

      var mapBrokerToViewModel = function(domainModel) {
        return {
          firstName: domainModel.first_name,
          lastName: domainModel.last_name,
          email: domainModel.email,
          phone: domainModel.phone
        };
      };

      var getCompanyBroker = function(companyId) {
        var deferred = $q.defer();

        employerWorkerRepository.get({companyId: companyId}).$promise
        .then(function(companyUser) {
          var brokers = _.filter(companyUser.user_roles, function(user) {
            return user.company_user_type === 'broker';
          });

          var brokerPromises = [];
          _.each(brokers, function(broker) {
            var promise = PersonService.getSelfPersonInfo(broker.user.id);
            brokerPromises.push(promise);
          });

          asyncCall(brokerPromises, null, function(response) {
            var brokerPersons = [];
            _.each(response, function(broker) {
              brokerPersons.push(viewModel);
            });

            deferred.resolve(brokerPersons);
          });
        });
        return deferred.promise;
      };

      return {
         saveCompanyInfo: saveCompanyInfo,
         getCompanyInfo: getCompanyInfo,
         getCompanyBroker: getCompanyBroker
      };
   }
]);
