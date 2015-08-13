var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('SupplementalLifeInsuranceService',
    ['$q',
    'SupplementalLifeInsuranceRepository',
    'SupplementalLifeInsuranceConditionService',
    'PersonService',
    function (
        $q,
        SupplementalLifeInsuranceRepository,
        SupplementalLifeInsuranceConditionService,
        PersonService){

        // Constants
        // Assumption: rateTableMinAgeLimit + N * rateTableAgeInterval = rateTableMaxAgeLimit
        //             i.e. no "fractions" at the end.
        var rateTableMinAgeLimit = 20;
        var rateTableMaxAgeLimit = 85;
        var rateTableAgeInterval = 5;

        // An artificial age max limit to support the notion of
        // 'X age and above'.
        var ageRangeMax = 200;

        var mapPlanDomainToViewModel = function(planDomainModel) {
            var viewModel = {};

            viewModel.planId = planDomainModel.id;
            viewModel.planName = planDomainModel.name;
            viewModel.planRates = mapPlanRateTableDomainToViewModel(planDomainModel.supplemental_life_insurance_plan_rate);
            viewModel.useEmployeeAgeForSpouse = planDomainModel.use_employee_age_for_spouse;

            return viewModel;
        };

        var mapCompanyPlanDomainToViewModel = function(companyPlanDomainModel) {
            var viewModel = companyPlanDomainModel.supplemental_life_insurance_plan ?
                mapPlanDomainToViewModel(companyPlanDomainModel.supplemental_life_insurance_plan) :
                {};

            viewModel.companyPlanId = companyPlanDomainModel.id;
            viewModel.createdDateForDisplay = moment(companyPlanDomainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.company = companyPlanDomainModel.company;

            return viewModel;
        };

        var mapPersonCompanyPlanDomainToViewModel = function(personCompanyPlanDomainModel, company) {
            var viewModel = personCompanyPlanDomainModel.company_supplemental_life_insurance_plan ?
                mapCompanyPlanDomainToViewModel(personCompanyPlanDomainModel.company_supplemental_life_insurance_plan) :
                {};

            viewModel.personCompanyPlanId = personCompanyPlanDomainModel.id;
            viewModel.planOwner = personCompanyPlanDomainModel.person;
            viewModel.lastUpdateDateTime = moment(personCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
            if(!personCompanyPlanDomainModel.waived){
                viewModel.selfPlanCondition = mapConditionDomainToViewModel(personCompanyPlanDomainModel.self_condition);
                viewModel.spousePlanCondition = mapConditionDomainToViewModel(personCompanyPlanDomainModel.spouse_condition);
                viewModel.selfElectedAmount = personCompanyPlanDomainModel.self_elected_amount;
                viewModel.spouseElectedAmount = personCompanyPlanDomainModel.spouse_elected_amount;
                viewModel.childElectedAmount = personCompanyPlanDomainModel.child_elected_amount;
                viewModel.selfPremiumPerMonth = (personCompanyPlanDomainModel.self_premium_per_month * company.pay_period_definition.month_factor).toFixed(2);
                viewModel.spousePremiumPerMonth = (personCompanyPlanDomainModel.spouse_premium_per_month * company.pay_period_definition.month_factor).toFixed(2);
                viewModel.childPremiumPerMonth = (personCompanyPlanDomainModel.child_premium_per_month * company.pay_period_definition.month_factor).toFixed(2);
            }
            viewModel.beneficiaryList = mapBeneficiaryListDomainToViewModel(personCompanyPlanDomainModel.suppl_life_insurance_beneficiary);
            viewModel.selected = personCompanyPlanDomainModel.selected;
            viewModel.waived = personCompanyPlanDomainModel.waived;

            return viewModel;
        };

        var mapBeneficiaryDomainToViewModel = function(beneficiaryDomainModel) {
            var viewModel = {};

            viewModel.beneficiaryId = beneficiaryDomainModel.id;
            viewModel.firstName = beneficiaryDomainModel.first_name;
            viewModel.middleName = beneficiaryDomainModel.middle_name;
            viewModel.lastName = beneficiaryDomainModel.last_name;
            viewModel.relationshipToPlanOwner = beneficiaryDomainModel.relationship;
            viewModel.email = beneficiaryDomainModel.email;
            viewModel.phone = beneficiaryDomainModel.phone;
            viewModel.benefitAllocationPercentage = beneficiaryDomainModel.percentage;
            viewModel.beneficiaryTier = beneficiaryDomainModel.tier;
            viewModel.personCompanyLifeInsurancePlanId = beneficiaryDomainModel.person_comp_suppl_life_insurance_plan;

            return viewModel;
        };

        var mapBeneficiaryListDomainToViewModel = function(beneficiaryListDomainModel) {
            var viewModel = {};
            viewModel.mainBeneficiaries = [];
            viewModel.contingentBeneficiaries = [];

            _.each(beneficiaryListDomainModel, function(beneficiaryDomainModel)
                {
                    var beneficiary = mapBeneficiaryDomainToViewModel(beneficiaryDomainModel);
                    if (beneficiary.beneficiaryTier === '1') {
                        viewModel.mainBeneficiaries.push(beneficiary);
                    } else {
                        viewModel.contingentBeneficiaries.push(beneficiary);
                    }
                });

            return viewModel;
        };

        var mapConditionDomainToViewModel = function(conditionDomainModel) {
            var viewModel = {};

            viewModel.conditionId = conditionDomainModel.id;
            viewModel.name = conditionDomainModel.name;
            viewModel.description = conditionDomainModel.description;

            return viewModel;
        };

        var mapPlanRateDomainToViewModel = function(planRateDomainModel) {
            var viewModel = {};

            viewModel.planRateId = planRateDomainModel.id;
            viewModel.supplementalLifeInsurancePlanId = planRateDomainModel.supplemental_life_insurance_plan;
            viewModel.ageMin = planRateDomainModel.age_min ? Number(planRateDomainModel.age_min) : -1;
            viewModel.ageMax = planRateDomainModel.age_max ? Number(planRateDomainModel.age_max) : ageRangeMax;
            viewModel.bindType = planRateDomainModel.bind_type;
            viewModel.ratePer10000 = planRateDomainModel.rate;
            viewModel.benefitReductionPercentage = planRateDomainModel.benefit_reduction_percentage || 0;
            viewModel.planCondition = mapConditionDomainToViewModel(planRateDomainModel.condition);

            return viewModel;
        };

        var mapPlanRateTableDomainToViewModel = function(planRateTableDomainModel) {

            // First map all entries to view model
            var entries = [];
            _.each(planRateTableDomainModel, function(planRateDomainModel)
                {
                    entries.push(mapPlanRateDomainToViewModel(planRateDomainModel));
                });

            // Now sort the list by min age
            var sortedEntries = _.sortBy(entries, 'ageMin');

            // It should be good enough to hard code the condition/bindType
            // combinations for view model mapping.
            var employeeTobaccoRateTable = [];
            var employeeNonTobaccoRateTable = [];
            var spouseTobaccoRateTable = [];
            var spouseNonTobaccoRateTable = [];
            var childRate = {};

            // Now populate the view model
            _.each(sortedEntries, function(rate)
                {
                    if (rate.bindType === "self") {
                        if (rate.planCondition.name === "Tobacco") {
                            employeeTobaccoRateTable.push(rate);
                        } else if (rate.planCondition.name === "Non-Tobacco") {
                            employeeNonTobaccoRateTable.push(rate);
                        }
                    } else if (rate.bindType === "spouse") {
                        if (rate.planCondition.name === "Tobacco") {
                            spouseTobaccoRateTable.push(rate);
                        } else if (rate.planCondition.name === "Non-Tobacco") {
                            spouseNonTobaccoRateTable.push(rate);
                        }
                    } else if (rate.bindType === "dependent") {
                        childRate = rate;
                    }
                });

            var viewModel = {};
            viewModel.employeeRateTable = combineRateTablesByAgeRanges(
                employeeTobaccoRateTable, employeeNonTobaccoRateTable);
            viewModel.spouseRateTable = combineRateTablesByAgeRanges(
                spouseTobaccoRateTable, spouseNonTobaccoRateTable);
            viewModel.childRate = childRate;

            return viewModel;
        };

        var mapPlanViewToDomainModel = function(planViewModel) {
            var domainModel = {};

            domainModel.id = planViewModel.planId;
            domainModel.name = planViewModel.planName;
            domainModel.supplemental_life_insurance_plan_rate = mapPlanRateTableViewToDomainModel(planViewModel.planRates)
            domainModel.use_employee_age_for_spouse = planViewModel.useEmployeeAgeForSpouse;

            return domainModel;
        };

        var mapCompanyPlanViewToDomainModel = function(companyPlanViewModel) {
            var domainModel = {};

            domainModel.id = companyPlanViewModel.companyPlanId;
            domainModel.company = companyPlanViewModel.company;

            domainModel.supplemental_life_insurance_plan = mapPlanViewToDomainModel(companyPlanViewModel);

            return domainModel;
        };

        var mapPersonCompanyPlanViewToDomainModel = function(personCompanyPlanViewModel) {
            var domainModel = {};

            domainModel.id = personCompanyPlanViewModel.personCompanyPlanId;
            domainModel.person = personCompanyPlanViewModel.planOwner;
            if(personCompanyPlanViewModel.companyPlanId){
                domainModel.self_condition = mapConditionViewToDomainModel(personCompanyPlanViewModel.selfPlanCondition);
                domainModel.spouse_condition = mapConditionViewToDomainModel(personCompanyPlanViewModel.spousePlanCondition);
                domainModel.self_elected_amount = personCompanyPlanViewModel.selfElectedAmount;
                domainModel.spouse_elected_amount = personCompanyPlanViewModel.spouseElectedAmount;
                domainModel.child_elected_amount = personCompanyPlanViewModel.childElectedAmount;
                domainModel.self_premium_per_month = personCompanyPlanViewModel.selfPremiumPerMonth;
                domainModel.spouse_premium_per_month = personCompanyPlanViewModel.spousePremiumPerMonth;
                domainModel.child_premium_per_month = personCompanyPlanViewModel.childPremiumPerMonth;

                domainModel.company_supplemental_life_insurance_plan = mapCompanyPlanViewToDomainModel(personCompanyPlanViewModel);

                domainModel.suppl_life_insurance_beneficiary = mapBeneficiaryListViewToDomainModel(personCompanyPlanViewModel.beneficiaryList);
            }
            else{
                domainModel.company_supplemental_life_insurance_plan = null;
            }
            domainModel.record_reason_note = personCompanyPlanViewModel.updateReason.notes;
            domainModel.record_reason = personCompanyPlanViewModel.updateReason.selectedReason.id;

            return domainModel;
        };

        var mapBeneficiaryViewToDomainModel = function(beneficiaryViewModel) {
            var domainModel = {};

            domainModel.id = beneficiaryViewModel.beneficiaryId;
            domainModel.first_name = beneficiaryViewModel.firstName;
            domainModel.middle_name = beneficiaryViewModel.middleName;
            domainModel.last_name = beneficiaryViewModel.lastName;
            domainModel.relationship = beneficiaryViewModel.relationshipToPlanOwner;
            domainModel.email = beneficiaryViewModel.email;
            domainModel.phone = beneficiaryViewModel.phone;
            domainModel.percentage = beneficiaryViewModel.benefitAllocationPercentage;
            domainModel.tier = beneficiaryViewModel.beneficiaryTier;
            domainModel.person_comp_suppl_life_insurance_plan = beneficiaryViewModel.personCompanyLifeInsurancePlanId;

            return domainModel;
        };

        var mapBeneficiaryListViewToDomainModel = function(beneficiaryListViewModel) {
            var domainModel = [];

            _.each(beneficiaryListViewModel.mainBeneficiaries, function(beneficiaryViewModel)
                {
                    domainModel.push(mapBeneficiaryViewToDomainModel(beneficiaryViewModel));
                });

            _.each(beneficiaryListViewModel.contingentBeneficiaries, function(beneficiaryViewModel)
                {
                    domainModel.push(mapBeneficiaryViewToDomainModel(beneficiaryViewModel));
                });

            return domainModel;
        };

        var mapConditionViewToDomainModel = function(conditionViewModel) {

            // We only need plain ID for this
            return conditionViewModel.conditionId;
        };

        var mapPlanRateViewToDomainModel = function(planRateViewModel) {
            var domainModel = {};

            domainModel.id = planRateViewModel.planRateId;
            domainModel.supplemental_life_insurance_plan = planRateViewModel.supplementalLifeInsurancePlanId;
            domainModel.age_min = planRateViewModel.ageMin < 0 ? null : planRateViewModel.ageMin;
            domainModel.age_max = planRateViewModel.ageMax >= ageRangeMax ? null : planRateViewModel.ageMax;
            domainModel.bind_type = planRateViewModel.bindType;
            domainModel.rate = planRateViewModel.ratePer10000;
            domainModel.benefit_reduction_percentage = planRateViewModel.benefitReductionPercentage <= 0
                                                        ? null
                                                        : planRateViewModel.benefitReductionPercentage;
            domainModel.condition = planRateViewModel.planCondition.conditionId;

            return domainModel;
        };

        var mapPlanRateTableViewToDomainModel = function(planRateTableViewModel) {
            if (!planRateTableViewModel) {
                return null;
            }

            var domainModel = [];

            _.each(planRateTableViewModel.employeeRateTable, function(combinedRateViewModel)
                {
                    if (combinedRateViewModel.tobaccoRate) {
                        combinedRateViewModel.tobaccoRate.benefitReductionPercentage = combinedRateViewModel.benefitReductionPercentage;
                        domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.tobaccoRate));
                    }
                    if (combinedRateViewModel.nonTobaccoRate) {
                        combinedRateViewModel.nonTobaccoRate.benefitReductionPercentage = combinedRateViewModel.benefitReductionPercentage;
                        domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.nonTobaccoRate));
                    }
                });
            _.each(planRateTableViewModel.spouseRateTable, function(combinedRateViewModel)
                {
                    if (combinedRateViewModel.tobaccoRate) {
                        combinedRateViewModel.tobaccoRate.benefitReductionPercentage = combinedRateViewModel.benefitReductionPercentage;
                        domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.tobaccoRate));
                    }
                    if (combinedRateViewModel.nonTobaccoRate) {
                        combinedRateViewModel.nonTobaccoRate.benefitReductionPercentage = combinedRateViewModel.benefitReductionPercentage;
                        domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.nonTobaccoRate));
                    }
                });
            domainModel.push(mapPlanRateViewToDomainModel(planRateTableViewModel.childRate));

            return domainModel;
        };

        //////////////////////////////////////////////////////////////////
        // Start : Plan rate table helpers
        //////////////////////////////////////////////////////////////////

        /**
            Combine the given tobacco and non-tobacco rate tables by age range.
            e.g. tables were in the form
                age_range  tobacco_rate     age_range non_tobacco_rate
            and result would be a list with entries in the form
                age_range   tobacco_rate    non_tobacco_rate
        */
        var combineRateTablesByAgeRanges = function(tobaccoTable, nonTobaccoTable) {
            var map = {};

            _.each(tobaccoTable, function(item) {
                var key = item.ageMin+':'+item.ageMax;
                map[key] = {
                    'ageMin':item.ageMin,
                    'ageMax':item.ageMax,
                    'tobaccoRate': item
                };
            });

            _.each(nonTobaccoTable, function(item) {
                var key = item.ageMin+':'+item.ageMax;
                if (map[key]) {
                    map[key].nonTobaccoRate = item;
                } else {
                    // This should not happen at all, but
                    // just for the sake of not making too
                    // many assumptions, and let logic be
                    // generic where possible...
                    map[key] = {
                        'ageMin':item.ageMin,
                        'ageMax':item.ageMax,
                        'nonTobaccoRate': item
                    };
                }
            });

            var resultRateList = [];
            for (var k in map) {
                var item = map[k];

                // For display age range text
                item.getAgeRangeForDisplay = function() { return getAgeRangeForDisplay(this); };

                // Solicit the benefit reduction percentage
                // Note: This is under the assumption that the benefit reduction
                //       percentage is consistent/shared between tobacco and
                //       non-tobacco rate entries.
                item.benefitReductionPercentage = item.nonTobaccoRate.benefitReductionPercentage;

                resultRateList.push(item);
            }

            return _.sortBy(resultRateList, 'ageMin');
        };

        /**
            Setup a blank rate table, per the desired structure
        */
        var getBlankRateTable = function(bindType, planCondition) {
            // Populate the list of age ranges for the rate table
            // based on the constants defined above.
            var ageRanges = [];
            if (rateTableMinAgeLimit > 0) {
                ageRanges.push({"min": -1, "max": rateTableMinAgeLimit - 1});
            }
            for (i = rateTableMinAgeLimit; i+rateTableAgeInterval <= rateTableMaxAgeLimit; i=i+rateTableAgeInterval) {
                ageRanges.push({"min": i, "max":i+rateTableAgeInterval-1});
            }
            ageRanges.push({"min": rateTableMaxAgeLimit, "max": ageRangeMax});

            // Construct the rate table based on the inputs and the
            // age ranges
            var rateTable = [];
            _.each(ageRanges, function(ageRange) {
                rateTable.push({
                    'ageMin' : ageRange.min,
                    'ageMax' : ageRange.max,
                    'bindType' : bindType,
                    'planCondition' : planCondition,
                    'benefitReductionPercentage': 0
                });
            });

            return rateTable;
        };

        var getBlankRateTableViewModel = function() {
            var deferred = $q.defer();

            // First get the full condition data from server
            SupplementalLifeInsuranceConditionService.getConditions().then(function(conditions) {

                var employeeTobaccoRateTable = getBlankRateTable('self', conditions['Tobacco']);
                var employeeNonTobaccoRateTable = getBlankRateTable('self', conditions['Non-Tobacco']);
                var spouseTobaccoRateTable = getBlankRateTable('spouse', conditions['Tobacco']);
                var spouseNonTobaccoRateTable = getBlankRateTable('spouse', conditions['Non-Tobacco']);

                var viewModel = {};
                viewModel.employeeRateTable = combineRateTablesByAgeRanges(
                    employeeTobaccoRateTable, employeeNonTobaccoRateTable);
                viewModel.spouseRateTable = combineRateTablesByAgeRanges(
                    spouseTobaccoRateTable, spouseNonTobaccoRateTable);
                viewModel.childRate = {
                        'ageMin' : -1,
                        'ageMax' : ageRangeMax,
                        'bindType' : 'dependent',
                        'planCondition' : conditions['Unknown']
                    };

                deferred.resolve(viewModel);
            });

            return deferred.promise;
        };

        var getAgeRangeForDisplay = function(rateViewModel) {
            if (rateViewModel.ageMin >= 0 && rateViewModel.ageMax < ageRangeMax){
                return rateViewModel.ageMin + ' through ' + rateViewModel.ageMax;
            } else if (rateViewModel.ageMin >= 0) {
                return rateViewModel.ageMin + ' and above';
            } else if (rateViewModel.ageMax < ageRangeMax) {
                return rateViewModel.ageMax + ' and under';
            } else {
                return 'All';
            }
        };

        //////////////////////////////////////////////////////////////////
        // End : Plan rate table helpers
        //////////////////////////////////////////////////////////////////

        var getPlansForCompany = function(companyId) {
            var deferred = $q.defer();

            SupplementalLifeInsuranceRepository.CompanyPlanByCompany.query({companyId:companyId})
            .$promise.then(function(plans) {
                var planViewModels = [];
                _.each(plans, function(companyPlan) {
                    planViewModels.push(mapCompanyPlanDomainToViewModel(companyPlan));
                });
                deferred.resolve(planViewModels);
            },
            function(error){
                deferred.reject(error);
            });

            return deferred.promise;
        }

        return {
            planBindTypes: ['self', 'spouse', 'dependent'],

            getPlansForCompany: getPlansForCompany,

            getBlankPlanForCompany: function(companyId) {
                var deferred = $q.defer();

                getBlankRateTableViewModel().then(function(blankRates) {
                    var blankCompanyPlan = {};
                    // Setup company
                    blankCompanyPlan.company = companyId;
                    // Setup a blank but structured rate table
                    blankCompanyPlan.planRates = blankRates;
                    blankCompanyPlan.useEmployeeAgeForSpouse = false;

                    deferred.resolve(blankCompanyPlan);
                });

                return deferred.promise;
            },

            addPlanForCompany: function(companyPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                var companyPlanDomainModel = mapCompanyPlanViewToDomainModel(companyPlanToSave);

                // Create the plan first
                SupplementalLifeInsuranceRepository.PlanById.save({id:companyId}, companyPlanDomainModel.supplemental_life_insurance_plan)
                .$promise.then(function(newPlan){

                    // Now enroll the company with this plan
                    companyPlanDomainModel.supplemental_life_insurance_plan = newPlan.id;
                    companyPlanDomainModel.company = companyId;

                    SupplementalLifeInsuranceRepository.CompanyPlanById.save({id:companyId}, companyPlanDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });

                },
                function(error){
                    deferred.reject(error)
                });

                return deferred.promise;
            },

            deleteCompanyPlan: function(companyPlanIdToDelete) {
                var deferred = $q.defer();

                SupplementalLifeInsuranceRepository.CompanyPlanById.delete({id:companyPlanIdToDelete})
                .$promise.then(function(response) {
                    deferred.resolve(response);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            getPlanByUser: function(userId, company, getBlankPlanIfNoneFound) {
                var deferred = $q.defer();
                getPlansForCompany(company.id).then(function(plans){
                    if(!plans || plans.length <= 0){
                        deferred.resolve(undefined);
                    }
                    else{
                        PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
                            SupplementalLifeInsuranceRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
                            .$promise.then(function(personPlans) {
                                if (personPlans.length > 0) {
                                    // Found existing person enrolled plans, for now, take the first
                                    // one.
                                    var personPlan = personPlans[0];
                                    personPlan.selected = true;
                                    personPlan.waived = !personPlan.company_supplemental_life_insurance_plan
                                    deferred.resolve(mapPersonCompanyPlanDomainToViewModel(personPlans[0], company));
                                } else {
                                    // The person does not have enrolled plans yet.
                                    // If indicated so, construct and return an structured
                                    // blank person plan.
                                    // Or else, return null;
                                    if (getBlankPlanIfNoneFound) {
                                        var blankPersonPlan = {};
                                        // Setup person plan owner
                                        blankPersonPlan.planOwner = personInfo.id;
                                        // Setup a blank but structured beneficiary list
                                        blankPersonPlan.beneficiaryList = mapBeneficiaryListDomainToViewModel([]);
                                        // Setup default values for elected amounts
                                        blankPersonPlan.selfElectedAmount = 0;
                                        blankPersonPlan.spouseElectedAmount = 0;
                                        blankPersonPlan.childElectedAmount = 0;
                                        // Setup flag to indicate current enrollment state
                                        blankPersonPlan.selected = false;
                                        blankPersonPlan.waived = false;

                                        deferred.resolve(blankPersonPlan);
                                    }
                                    else {
                                        deferred.resolve(null);
                                    }
                                }
                            },
                            function(error) {
                                deferred.reject(error);
                            });
                        },
                        function(error){
                            deferred.reject(error);
                        });
                    }
                });

                return deferred.promise;
            },

            savePersonPlan: function(personPlanToSave, updateReason) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                personPlanToSave.updateReason = updateReason;

                var planDomainModel = mapPersonCompanyPlanViewToDomainModel(personPlanToSave);

                // "Flatten out" any nested structure for the POST to work
                if(planDomainModel.company_supplemental_life_insurance_plan){
                    planDomainModel.company_supplemental_life_insurance_plan = planDomainModel.company_supplemental_life_insurance_plan.id;
                }

                if (planDomainModel.id){
                    SupplementalLifeInsuranceRepository.CompanyPersonPlanById.update({id:planDomainModel.id}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                } else {
                    SupplementalLifeInsuranceRepository.CompanyPersonPlanById.save({id:personPlanToSave.planOwner}, planDomainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(response);
                    },
                    function(error){
                        deferred.reject(error);
                    });
                }

                return deferred.promise;
            },
        };
    }
]);
