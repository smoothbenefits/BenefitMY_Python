var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('WorkersCompService',
  ['$q',
    'PhraseologyRepository',
   function WorkersCompService(
    $q,
    PhraseologyRepository) {

        // A cached copy of the full phraseology list
        var _cachedAllPhraseologys = [];

        var GetAllPhraseologys = function() {
            var deferred = $q.defer();

            if (_cachedAllPhraseologys.length > 0) {
                deferred.resolve(_cachedAllPhraseologys);
            } else {
                PhraseologyRepository.All.query().$promise.then(
                    function(allPhraseologys) {
                        _cachedAllPhraseologys = allPhraseologys;
                        deferred.resolve(_cachedAllPhraseologys);
                    },
                    function(errors) {
                        deferred.reject(errors);
                    }
                );
            }

            return deferred.promise;
        };

        var GetCompanyDepartments = function(companyId) {
            return PhraseologyRepository.CompanyPhraseologysByCompany.query({companyId:companyId})
                .$promise.then(
                    function(companyPhraseologys) {
                        return companyPhraseologys;
                    }
                );
        };

        var DeleteCompanyPhraseology = function(companyPhraseology) {
            return PhraseologyRepository.CompanyPhraseologyById.delete({id:companyPhraseology.id})
            .$promise.then(function(response) {
                return response;
            });
        };

        var SaveCompanyPhraseology = function(companyPhraseology) {
            var domainSaveModel = mapCompanyPhraseologyToDomainSaveModel(companyPhraseology);
            
            if (domainSaveModel.id) {
                return PhraseologyRepository.CompanyPhraseologyById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(function(resultCompanyPhraseology) {
                    return resultCompanyPhraseology;
                });
            } else {
                return PhraseologyRepository.CompanyPhraseologyById.save(domainSaveModel)
                .$promise.then(function(resultCompanyPhraseology) {
                    return resultCompanyPhraseology;
                });
            }
        };

        var GetBlankCompanyDepartmentByCompany = function(company) {
            return {
                company: company.id
            };
        };

        var mapCompanyPhraseologyToDomainSaveModel = function(viewModel) {
            return {
                id: viewModel.id,
                company: viewModel.company,
                phraseology: viewModel.phraseology.id,
                description: viewModel.description
            };
        };

        return {
            GetAllPhraseologys: GetAllPhraseologys,
            GetCompanyDepartments: GetCompanyDepartments,
            GetBlankCompanyDepartmentByCompany: GetBlankCompanyDepartmentByCompany,
            DeleteCompanyPhraseology: DeleteCompanyPhraseology,
            SaveCompanyPhraseology: SaveCompanyPhraseology
        };
    }
]);
