var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyService',
   ['$q', 'companyRepository', 'CompanyUserDetailRepository', 'MonthsInYear',
   function($q, companyRepository, CompanyUserDetailRepository, MonthsInYear){

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
        viewModel.open_enrollment_month = _.findWhere(MonthsInYear,{id: domainModel.open_enrollment_month});
        viewModel.open_enrollment_day = domainModel.open_enrollment_day;
        viewModel.open_enrollment_length_in_days = domainModel.open_enrollment_length_in_days;

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
        apiClient.open_enrollment_month = viewModel.open_enrollment_month ? viewModel.open_enrollment_month.id : null;
        apiClient.open_enrollment_day = viewModel.open_enrollment_day;
        apiClient.open_enrollment_length_in_days = viewModel.open_enrollment_length_in_days;
        var apiContact = {};
        apiContact.first_name = viewModel.contact.first_name;
        apiContact.last_name = viewModel.contact.last_name;
        apiContact.email = viewModel.contact.email;
        apiContact.password = viewModel.contact.password;
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

        // default_benefit_group is a semicolon delimited string
        if(viewModel.default_benefit_group){
          var groups = [];
          _.each(viewModel.default_benefit_group.split(";"), function(group) {
            var groupName = group.trim();
            // Remove empty group names
            if (groupName) {
              groups.push(groupName);
            }
          });
          apiClient.default_benefit_groups = groups;
        }

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

        if ( !viewModel.company.id &&
             !(viewModel.default_benefit_group && viewModel.default_benefit_group.trim())
           ) {
          return { isValid: false, message: "Benefit group is required."};
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

      var mapCompanyBrokerToViewModel = function(domainBroker) {
        var viewBroker = {
          firstName: domainBroker.user.first_name,
          lastName: domainBroker.user.last_name,
          email: domainBroker.user.email
        };

        var person = _.find(domainBroker.user.family, function(member) {
          return member.relationship === 'self';
        });

        if (person && person.phones && person.phones.length > 0) {
          viewBroker.phone = person.phones[0].number;
        } else {
          viewBroker.phone = 'Not Available';
        }

        return viewBroker;
      };

      var getCompanyBroker = function(companyId) {
        var deferred = $q.defer();

        CompanyUserDetailRepository.ByCompany.get({comp_id: companyId, role: 'broker'})
        .$promise.then(function(response) {
          var brokers = [];

          _.each(response.company_broker, function(broker) {
            var viewBroker = mapCompanyBrokerToViewModel(broker);
            brokers.push(viewBroker);
          });

          deferred.resolve(brokers);
        }).catch(function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      var mapCompanyAdminToViewModel = function(admin) {
        return angular.copy(admin.user);
      }

      var getCompanyAdmin = function(companyId) {
        var deferred = $q.defer();

        CompanyUserDetailRepository.ByCompany.get({comp_id: companyId, role: 'admin'})
        .$promise.then(function(response) {
          var admins = [];

          _.each(response.company_broker, function(admin) {
            var viewAdmin = mapCompanyAdminToViewModel(admin);
            admins.push(viewAdmin);
          });

          deferred.resolve(admins);
        }).catch(function(error) {
          deferred.reject(error);
        });

        return deferred.promise;
      };

      return {
         saveCompanyInfo: saveCompanyInfo,
         getCompanyInfo: getCompanyInfo,
         getCompanyBroker: getCompanyBroker,
         getCompanyAdmin: getCompanyAdmin
      };
   }
]);
