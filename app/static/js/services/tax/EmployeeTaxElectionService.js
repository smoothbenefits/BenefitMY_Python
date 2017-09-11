var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployeeTaxElectionService',
    ['$q',
    'EmployeeTaxElectionRepository',
    'UserService',
    function (
        $q, 
        EmployeeTaxElectionRepository,
        UserService){

        var TaxElectionSupportedStates = ['MA', 'RI'];

        var mapDomainToViewModel = function(electionDomainModel) {
            // Serve as a place-holder for additional data transformation for now
            // Just return the original, along with some utility functions attached
            
            var viewModel = electionDomainModel;
            return _attachUtilitiesToViewModel(viewModel);
        };

        var _attachUtilitiesToViewModel = function(viewModel) {
            viewModel.isValid = function() {
                return isValidTaxElection(this);
            };
            viewModel.getCreatedTimeStampForDisplay = function() {
                return _getTimeForDisplay(this.created_at);
            };
            viewModel.getUpdatedTimeStampForDisplay = function() {
                return _getTimeForDisplay(this.updated_at);
            };
            viewModel.isNew = function() {
                return self.isNewElection; 
            };
            return viewModel;
        };

        var mapViewToDomainModel = function(electionViewModel) {
            // Serve as a place-holder for additional data transformation for now
            // Just return the original 
            return electionViewModel;
        };

        var getTaxElectionsByEmployee = function(employeeUserId) {
            var deferred = $q.defer();

            EmployeeTaxElectionRepository.ByEmployee.query({userId:employeeUserId})
            .$promise.then(function(elections) {
                var electionViewModels = [];
                _.each(elections, function(election) {
                    electionViewModels.push(mapDomainToViewModel(election));
                });
                var sortedCollection = _.sortBy(electionViewModels, 'state');
                deferred.resolve(_.sortBy(sortedCollection));
            },
            function(error){
                deferred.reject(error);
            });

            return deferred.promise;
        };

        var deleteTaxElection = function(electionViewModel) {
            return EmployeeTaxElectionRepository.ByEmployeeAndState.delete(
                {userId: electionViewModel.user, state:electionViewModel.state}
            ).$promise.then(function(response) {
                return response;
            });
        };

        var saveTaxElection = function(electionViewModel) {
            var deferred = $q.defer();

            if (!electionViewModel.isValid()) {
                deferred.reject('The election is not valid to save.');
            } else {
                var domainModel = mapViewToDomainModel(electionViewModel);
                if(electionViewModel.isNew()) {
                    // We do POST here as this is to create a new election record
                    EmployeeTaxElectionRepository.ByEmployeeAndState.save(
                        {userId: electionViewModel.user, state:electionViewModel.state},
                        domainModel,
                        function(successResponse) {
                            deferred.resolve(successResponse);
                        }
                    );
                } else {
                    // We do a PUT here as this is to update an existing record
                    EmployeeTaxElectionRepository.ByEmployeeAndState.update(
                        {userId: electionViewModel.user, state:electionViewModel.state},
                        domainModel,
                        function(successResponse) {
                            deferred.resolve(successResponse);
                        }
                    );
                }
            }

            return deferred.promise;
        };

        var isValidTaxElection = function(taxElection) {
            if (!taxElection
                || !taxElection.state
                || !taxElection.user
                || !taxElection.tax_election_data) {
                return false;
            }

            if (!_.contains(TaxElectionSupportedStates, taxElection.state)) {
                return false;
            }

            var validator = _getElectionValidator(taxElection.state);
            if (!validator) {
                return false;
            }

            return validator(taxElection);
        };

        var getBlankElection = function(userId, state) {
            if (!_.contains(TaxElectionSupportedStates, state)) {
                throw new Error('Specified state is not supported for tax election yet: ' + state);
            }

            var blankGenerator = _getBlankElectionGenerator(state);
            if (!blankGenerator) {
                throw new Error('Could not locate blank election generator for specified state: ' + state);
            }
            var model = blankGenerator(userId);

            // Mark the model to indicate that it is for a new election
            model.isNewElection = true;

            // Attach the common utilities
            return _attachUtilitiesToViewModel(model);
        };  

        var _getTimeForDisplay = function(dateTime) {
            if (!dateTime) {
                return null;
            }
            return moment(dateTime).format(DATE_FORMAT_STRING);
        };

        //////////////////////////////////////////////
        // Per-state tax election validation
        //////////////////////////////////////////////

        var _getElectionValidator = function(state) {
            var taxElectionValidatorMapping = {
                MA: _isValidTaxElectionForMA,
                RI: _isValidTaxElectionForRI
            };

            return taxElectionValidatorMapping[state];
        };

        var _isValidTaxElectionForMA = function(taxElection) {
            if (!taxElection
                || !taxElection.state === 'MA'
                || !taxElection.tax_election_data) {
                return false;
            }
            if (!taxElection.tax_election_data.personal_exemption == undefined
                || !_.contains([1, 2], taxElection.tax_election_data.personal_exemption)) {
                return false;
            }
            if (!taxElection.tax_election_data.spouse_exemption == undefined
                || !_.contains([0, 4, 5], taxElection.tax_election_data.spouse_exemption)) {
                return false;
            }
            if (!taxElection.tax_election_data.num_dependents == undefined
                || taxElection.tax_election_data.num_dependents < 0) {
                return false;
            }
            if (taxElection.tax_election_data.additional_witholding == undefined
                || taxElection.tax_election_data.additional_witholding < 0) {
                return false;
            }
            if (taxElection.tax_election_data.head_of_household == undefined
                || taxElection.tax_election_data.is_blind == undefined
                || taxElection.tax_election_data.is_spouse_blind == undefined
                ||taxElection.tax_election_data.is_fulltime_student == undefined) {
                return false;
            }
            return true;
        }

        var _isValidTaxElectionForRI = function(taxElection) {
            if (!taxElection
                || !taxElection.state === 'RI'
                || !taxElection.tax_election_data) {
                return false;
            }

            if (!taxElection.tax_election_data.num_dependents == undefined
                || taxElection.tax_election_data.num_dependents < 0) {
                return false;
            }
            if (taxElection.tax_election_data.additional_allowances == undefined
                || taxElection.tax_election_data.additional_allowances < 0) {
                return false;
            }
            if (taxElection.tax_election_data.additional_witholding == undefined
                || taxElection.tax_election_data.additional_witholding < 0) {
                return false;
            }
            
            if (taxElection.tax_election_data.is_not_dependent == undefined
                || taxElection.tax_election_data.spouse_is_dependent == undefined
                || taxElection.tax_election_data.is_exempt_status == undefined
                ||taxElection.tax_election_data.is_exempt_ms_status == undefined) {
                return false;
            }
            return true;
        }

        //////////////////////////////////////////////

        //////////////////////////////////////////////
        // Per-state blank election generation
        //////////////////////////////////////////////

        var _getBlankElectionGenerator = function(state) {
            var taxElectionBlankGeneratorMapping = {
                MA: _getBlankElectionForMA,
                RI: _getBlankElectionForRI
            };

            return taxElectionBlankGeneratorMapping[state];
        }  

        var _getBlankElectionForMA = function(userId) {
            var result = {}
            result.user = userId;
            result.state = 'MA';
            result.tax_election_data = {};

            // Now populate the election data with defaults

            // For now, the MVP, we do not setup any defaults, to 
            // force users to make explicit inputs for every field

            return result;
        }

        var _getBlankElectionForRI = function(userId) {
            var result = {}
            result.user = userId;
            result.state = 'RI';
            result.tax_election_data = {};

            // Now populate the election data with defaults

            // For now, the MVP, we do not setup any defaults, to 
            // force users to make explicit inputs for every field

            return result;
        }

        //////////////////////////////////////////////

        return {
            TaxElectionSupportedStates: TaxElectionSupportedStates,
            getTaxElectionsByEmployee: getTaxElectionsByEmployee,
            saveTaxElection: saveTaxElection,
            isValidTaxElection: isValidTaxElection,
            getBlankElection: getBlankElection,
            deleteTaxElection: deleteTaxElection
        };
    }
]);
