var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyDepartmentService',
  ['$q',
    'DepartmentRepository',
   function CompanyDepartmentService(
    $q,
    DepartmentRepository) {

        var GetCompanyDepartments = function(companyId) {
            return DepartmentRepository.CompanyDepartmentsByCompany.query({companyId:companyId})
                .$promise.then(departments => departments);
        };

        var DeleteCompanyDepartment = function(companyDepartment) {
            return DepartmentRepository.CompanyDepartmentById.delete({id:companyDepartment.id})
            .$promise.then(response => response);
        };

        var SaveCompanyDepartment = function(companyDepartment) {
            var domainSaveModel = mapCompanyDepartmentToDomainSaveModel(companyDepartment);

            if (domainSaveModel.id) {
                return DepartmentRepository.CompanyDepartmentById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(resultCompanyDepartment => resultCompanyDepartment);
            } else {
                return DepartmentRepository.CompanyDepartmentById.save(domainSaveModel)
                .$promise.then(resultCompanyDepartment => resultCompanyDepartment);
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
