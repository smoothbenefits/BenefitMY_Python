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

        var GetCompanyPhraseologies = function(companyId) {
            return PhraseologyRepository.CompanyPhraseologysByCompany.query({companyId:companyId})
                .$promise.then(
                    function(companyPhraseologys) {
                        return companyPhraseologys;
                    }
                );
        };

        /**
            This is a utility method to help getting a list of company phraseologies
            while also ensure that the given phraseology presents in the list.
            If the phraseology does not link to any of the existing phraseology
            definitions, mock out a phraeology definition on the fly and include it
            in the resultant list.
            The main use case for this is to ensure that employees' phraseology
            assignment can be cannonically represented in places where a phraeology
            definition is assumed.
        */
        var GetCompanyPhraseologiesWithPredefinedPhraseology = function(companyId, phraseologyToEnsure) {
            if(!phraseologyToEnsure) {
                return GetCompanyPhraseologies(companyId);
            } else {
                return GetCompanyPhraseologies(companyId).then(function(phraseologies) {
                    var found = _.some(phraseologies, function(phraseology) {
                        return phraseology.phraseology.id == phraseologyToEnsure.id;
                    });

                    if (!found) {
                        // Construct a company phraseology from the given phraseology and
                        // insert into the list
                        var insertPhraseology = {
                            company: companyId,
                            description: phraseologyToEnsure.phraseology,
                            phraseology: phraseologyToEnsure
                        };
                        phraseologies.push(insertPhraseology);
                    }

                    return phraseologies;
                })
            }
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

        var GetBlankCompanyPhraseologyByCompany = function(company) {
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

        var GetEmployeePhraseologys = function(employeePersonId) {
            return PhraseologyRepository.EmployeePhraseologysByPerson.query({personId:employeePersonId})
                .$promise.then(
                    function(employeePhraseologys) {
                        return employeePhraseologys;
                    }
                );
        };

        var GetActiveEmployeePhraseology = function(employeePersonId) {
            return GetEmployeePhraseologys(employeePersonId).then(
                function(employeePhraseologys) {
                    return _.find(employeePhraseologys, function(employeePhraseology) {
                        return employeePhraseology.is_active;
                    });
                }
            );
        };

        var DeleteEmployeePhraseology = function(employeePhraseology) {
            return PhraseologyRepository.EmployeePhraseologyById.delete({id:employeePhraseology.id})
            .$promise.then(function(response) {
                return response;
            });
        };

        var SaveEmployeePhraseology = function(employeePhraseology) {
            var domainSaveModel = mapEmployeePhraseologyToDomainSaveModel(employeePhraseology);

            if (domainSaveModel.id) {
                return PhraseologyRepository.EmployeePhraseologyById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(function(resultEmployeePhraseology) {
                    return resultEmployeePhraseology;
                });
            } else {
                return PhraseologyRepository.EmployeePhraseologyById.save(domainSaveModel)
                .$promise.then(function(resultEmployeePhraseology) {
                    return resultEmployeePhraseology;
                });
            }
        };

        var GetBlankEmployeePhraseologyByEmployeePerson = function(personId) {
            return {
                employee_person: personId
            };
        };

        var mapEmployeePhraseologyToDomainSaveModel = function(viewModel) {
            return {
                id: viewModel.id,
                employee_person: viewModel.employee_person,
                phraseology: viewModel.phraseology.id
            };
        };

        return {
            GetAllPhraseologys: GetAllPhraseologys,
            GetCompanyPhraseologies: GetCompanyPhraseologies,
            GetCompanyPhraseologiesWithPredefinedPhraseology: GetCompanyPhraseologiesWithPredefinedPhraseology,
            GetBlankCompanyPhraseologyByCompany: GetBlankCompanyPhraseologyByCompany,
            DeleteCompanyPhraseology: DeleteCompanyPhraseology,
            SaveCompanyPhraseology: SaveCompanyPhraseology,
            GetEmployeePhraseologys: GetEmployeePhraseologys,
            GetActiveEmployeePhraseology: GetActiveEmployeePhraseology,
            DeleteEmployeePhraseology: DeleteEmployeePhraseology,
            SaveEmployeePhraseology: SaveEmployeePhraseology,
            GetBlankEmployeePhraseologyByEmployeePerson: GetBlankEmployeePhraseologyByEmployeePerson
        };
    }
]);
