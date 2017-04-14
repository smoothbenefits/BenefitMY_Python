var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployerEmployeeManagementService',
  ['$q',
  'usersRepository',
  'CompensationService',
  'CompanyPersonnelsService',
  function ($q,
    usersRepository,
    CompensationService,
    CompanyPersonnelsService) {

    var employmentTypes = [
      {
        "name": "Full-time",
        "id": 1
      },
      {
        "name": "Part-time",
        "id": 2
      },
      {
        "name": "Contractor",
        "id": 3
      },
      {
        "name": "Intern",
        "id": 4
      },
      {
        "name": "Per Diem",
        "id": 5
      }
    ];

    var isFullTimeEmploymentType = function(employmentType) {
      return employmentType.id === 1;
    };

    var mapToEmployeeDomainModel = function(companyId, viewModel, templateFields){
      var compensation = {
          "person": null,
          "company": companyId,
          "annual_base_salary": viewModel.annual_base_salary,
          "projected_hour_per_month": viewModel.projected_hour_per_month,
          "hourly_rate": viewModel.hourly_rate,
          // Use date of hire as compensation effective date
          "effective_date": moment(viewModel.date_of_hire).startOf('day'),
          "increase_percentage": null
        };

      var domainModel = {
        "company_id": companyId,
        "company_user_type": "employee",
        "new_employee": viewModel.new_employee,
        "start_date": moment(viewModel.date_of_hire).format('YYYY-MM-DD'),
        "benefit_start_date": moment(viewModel.benefit_start_date).format('YYYY-MM-DD'),
        "create_docs": viewModel.create_docs,
        "send_email": viewModel.send_email,
        "doc_fields": templateFields,
        "email": viewModel.email,
        "first_name": viewModel.first_name,
        "last_name": viewModel.last_name,
        "compensation_info": compensation,
        "group_id": viewModel.group_id,
        "employee_number": viewModel.employee_number
      };

      if (viewModel.employment_type.id === 1) {
        domainModel.employment_type = "FullTime";
      } else if (viewModel.employment_type.id === 2) {
        domainModel.employment_type = "PartTime";
      } else if (viewModel.employment_type.id === 3) {
        domainModel.employment_type = "Contractor";
      } else if (viewModel.employment_type.id === 4) {
        domainModel.employment_type = "Intern";
      } else if (viewModel.employment_type.id === 5) {
        domainModel.employment_type = "PerDiem";
      }

      // Do not set password if selected "send email"
      if (!domainModel.send_email) {
        domainModel.password = viewModel.password;
      }

      if (viewModel.managerSelected && viewModel.managerSelected.id){
        domainModel.manager_id = viewModel.managerSelected.id
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

      // Date of hire is a required field
      if (!newEmployee.date_of_hire) {
        return false;
      }

      // If full time, annual base salary or hourly rate is required
      if (newEmployee.employment_type.id === 1 && !newEmployee.annual_base_salary
      && (!newEmployee.hourly_rate || !newEmployee.projected_hour_per_month)) {
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
        result.added = true;
        result.sentEmail = domainEmployeeModel.send_email;
        CompanyPersonnelsService.clearCache(companyId);
        deferred.resolve(result);
      }).catch(function(error) {
        result.added = false;
        result.sentEmail = false;
        result.messages = error.data;
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
