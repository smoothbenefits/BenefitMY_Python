var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyDivisionService',
  ['$q',
    'DivisionRepository',
   function CompanyDivisionService(
    $q,
    DivisionRepository) {

        var GetCompanyDivisions = function(companyId) {
            return DivisionRepository.CompanyDivisionsByCompany.query({companyId:companyId})
                .$promise.then(function (divisions) {
                    return divisions;
                });
        };

        var DeleteCompanyDivision = function(companyDivision) {
            return DivisionRepository.CompanyDivisionById.delete({id:companyDivision.id})
            .$promise.then(function (response) {
                return response;
            });
        };

        var SaveCompanyDivision = function(companyDivision) {
            var domainSaveModel = mapCompanyDivisionToDomainSaveModel(companyDivision);

            if (domainSaveModel.id) {
                return DivisionRepository.CompanyDivisionById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(function(resultCompanyDivision) {
                    return resultCompanyDivision;
                });
            } else {
                return DivisionRepository.CompanyDivisionById.save(domainSaveModel)
                .$promise.then(function(resultCompanyDivision) {
                    return resultCompanyDivision;
                });
            }
        };

        var GetBlankCompanyDivisionByCompanyId = function(companyId) {
            return {
                company: companyId
            };
        };

        var mapCompanyDivisionToDomainSaveModel = function(viewModel) {
            return angular.copy(viewModel);
        };

        return {
            GetCompanyDivisions: GetCompanyDivisions,
            GetBlankCompanyDivisionByCompanyId: GetBlankCompanyDivisionByCompanyId,
            DeleteCompanyDivision: DeleteCompanyDivision,
            SaveCompanyDivision: SaveCompanyDivision
        };
    }
]);
