var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyDepartmentService',
  ['$q',
    'DepartmentRepository',
   function CompanyDepartmentService(
    $q,
    DepartmentRepository) {

        var GetCompanyDepartments = function(companyId) {
            return DepartmentRepository.CompanyDepartmentsByCompany.query({companyId:companyId})
                .$promise.then(function (departments) {
                    return departments;
                });
        };

        var DeleteCompanyDepartment = function(companyDepartment) {
            return DepartmentRepository.CompanyDepartmentById.delete({id:companyDepartment.id})
            .$promise.then(function (response) {
                return response;
            });
        };

        var SaveCompanyDepartment = function(companyDepartment) {
            var domainSaveModel = mapCompanyDepartmentToDomainSaveModel(companyDepartment);

            if (domainSaveModel.id) {
                return DepartmentRepository.CompanyDepartmentById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(function(resultCompanyDepartment) {
                    return resultCompanyDepartment;
                });
            } else {
                return DepartmentRepository.CompanyDepartmentById.save(domainSaveModel)
                .$promise.then(function(resultCompanyDepartment) {
                    return resultCompanyDepartment;
                });
            }
        };

        var GetBlankCompanyDepartmentByCompanyId = function(companyId) {
            return {
                company: companyId
            };
        };

        var mapCompanyDepartmentToDomainSaveModel = function(viewModel) {
            return angular.copy(viewModel);
        };

        return {
            GetCompanyDepartments: GetCompanyDepartments,
            GetBlankCompanyDepartmentByCompanyId: GetBlankCompanyDepartmentByCompanyId,
            DeleteCompanyDepartment: DeleteCompanyDepartment,
            SaveCompanyDepartment: SaveCompanyDepartment
        };
    }
]);
