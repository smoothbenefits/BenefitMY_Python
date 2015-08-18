var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployerEmployeeManagementService',
  ['$q',
  'usersRepository',
  'CompensationService',
  function ($q, usersRepository, CompensationService) {

    var employmentTypes = [
      {
        "name": "Full-time",
        "id": 1
      },
      {
        "name": "Part-time",
        "id": 2
      }
    ];

    var isFullTimeEmploymentType = function(employmentType) {
      return employmentType.id === 1;
    };

    var mapToEmployeeDomainModel = function(companyId, viewModel, templateFields){
      var domainModel = {
        "company": companyId,
        "company_user_type": "employee",
        "new_employee": viewModel.new_employee,
        "create_docs": viewModel.create_docs,
        "send_email": viewModel.send_email,
        "annual_base_salary": viewModel.annual_base_salary,
        "hourly_rate": viewModel.hourly_rate,
        "effective_date": viewModel.effective_date,
        "projected_hour_per_month": viewModel.projected_hour_per_month,
        "fields": templateFields,
        "user": {
          "email": viewModel.email,
          "first_name": viewModel.first_name,
          "last_name": viewModel.last_name,
        }
      };

      if (viewModel.employment_type.id === 1) {
        domainModel.employment_type = "FullTime";
      } else if (viewModel.employment_type.id === 2) {
        domainModel.employment_type = "PartTime";
      }

      // Do not set password if selected "send email"
      if (!domainModel.send_email) {
        domainModel.user.password = viewModel.password;
      }
      return domainModel;
    };

    // Validate new employee view model
    var validateNewEmployeeInformation = function(newEmployee) {
      // If not send email, custom password is required
      if (!newEmployee.send_email && (!newEmployee.password || !newEmployee.password_confirm)){
        return false;
      }

      // First name, last name, email are required fields
      if (!newEmployee.first_name || !newEmployee.last_name || !newEmployee.email) {
        return false;
      }

      // Effective date for compensation is required
      if (!newEmployee.effective_date) {
        return false;
      }

      // If full time, annual base salary is required
      if (newEmployee.employment_type.id === 1 && !newEmployee.annual_base_salary) {
        return false;
      }

      // If part time, hourly rate and projected hour per month is required
      if (newEmployee.employment_type.id === 2 &&
      (!newEmployee.hourly_rate || !newEmployee.projected_hour_per_month)) {
        return false;
      }

      return true;
    };

    var addNewEmployee = function(companyId, newEmployee, templateFields) {
      var deferred = $q.defer();
      var result = {
        "added": false,
        "message": ""
      };

      if (!validateNewEmployeeInformation(newEmployee)) {
        result.message = "Data provided for the new employee is not valid.";
        deferred.reject(result);
      }

      var domainEmployeeModel = mapToEmployeeDomainModel(companyId, newEmployee, templateFields);

      // Create AuthUser and Person object for the new employee
      usersRepository.save(domainEmployeeModel).$promise
      .then(function(response) {
        return response.person.id;
      }).then(function(personId) {
        var compensation = {
          "person": personId,
          "company": companyId,
          "salary": domainEmployeeModel.annual_base_salary,
          "projected_hour_per_month": domainEmployeeModel.projected_hour_per_month,
          "hourly_rate": domainEmployeeModel.hourly_rate,
          "effective_date": domainEmployeeModel.effective_date,
          "increase_percentage": null,
        };

        // Add compensation information for the new employee
        CompensationService.addCompensationByPerson(compensation, personId, companyId)
        .then(function(response) {
          return response;
        });

        result.added = true;
        result.sentEmail = domainEmployeeModel.send_email;
        deferred.resolve(result);
      }).catch(function(error) {
        result.added = false;
        result.sentEmail = false;
        result.message = error;
        deferred.reject(result);
      });

      return deferred.promise;
    }

    return {
      EmploymentTypes : employmentTypes,
      IsFullTimeEmploymentType: isFullTimeEmploymentType,
      AddNewEmployee : addNewEmployee
    };
  }
]);
