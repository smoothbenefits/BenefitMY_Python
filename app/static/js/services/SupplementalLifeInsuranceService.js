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
        var rateTableMinAgeLimit = 25;
        var rateTableMaxAgeLimit = 25;
        var rateTableAgeInterval = 5;

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

        var mapPersonCompanyPlanDomainToViewModel = function(personCompanyPlanDomainModel) {
            var viewModel = personCompanyPlanDomainModel.company_supplemental_life_insurance_plan ? 
                mapCompanyPlanDomainToViewModel(personCompanyPlanDomainModel.company_supplemental_life_insurance_plan) :
                {};

            viewModel.personCompanyPlanId = personCompanyPlanDomainModel.id;
            viewModel.planOwner = personCompanyPlanDomainModel.person;
            viewModel.lastUpdateDateTime = moment(personCompanyPlanDomainModel.updated_at).format(DATE_FORMAT_STRING);
        
            viewModel.selfPlanCondition = mapConditionDomainToViewModel(personCompanyPlanDomainModel.self_condition);
            viewModel.spousePlanCondition = mapConditionDomainToViewModel(personCompanyPlanDomainModel.spouse_condition);
            viewModel.selfElectedAmount = personCompanyPlanDomainModel.self_elected_amount;
            viewModel.spouseElectedAmount = personCompanyPlanDomainModel.spouse_elected_amount;
            viewModel.childElectedAmount = personCompanyPlanDomainModel.child_elected_amount;
            viewModel.selfPremiumPerMonth = personCompanyPlanDomainModel.self_premium_per_month;
            viewModel.spousePremiumPerMonth = personCompanyPlanDomainModel.spouse_premium_per_month;
            viewModel.childPremiumPerMonth = personCompanyPlanDomainModel.child_premium_per_month;

            viewModel.beneficiaryList = mapBeneficiaryListDomainToViewModel(personCompanyPlanDomainModel.suppl_life_insurance_beneficiary);

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
            viewModel.ageMax = planRateDomainModel.age_max ? Number(planRateDomainModel.age_max) : -1;
            viewModel.bindType = planRateDomainModel.bind_type;
            viewModel.ratePer10000 = planRateDomainModel.rate;
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
            domainModel.self_condition = mapConditionViewToDomainModel(personCompanyPlanViewModel.selfPlanCondition);
            domainModel.spouse_condition = mapConditionViewToDomainModel(personCompanyPlanViewModel.spousePlanCondition);
            domainModel.self_elected_amount = personCompanyPlanViewModel.selfElectedAmount;
            domainModel.spouse_elected_amount = personCompanyPlanViewModel.spouseElectedAmount;
            domainModel.child_elected_amount = personCompanyPlanViewModel.childElectedAmount;
            domainModel.self_premium_per_month = personCompanyPlanViewModel.selfPremiumPerMonth;
            domainModel.spouse_premium_per_month = personCompanyPlanViewModel.spousePremiumPerMonth;
            domainModel.childPremiumPerMonth = personCompanyPlanDomainModel.childPremiumPerMonth;

            domainModel.company_ltd_insurance = mapCompanyPlanViewToDomainModel(userCompanyPlanViewModel);

            domainModel.suppl_life_insurance_beneficiary = mapBeneficiaryListViewToDomainModel(personCompanyPlanDomainModel.beneficiaryList);

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
            var domainModel = {};

            domainModel.id = conditionViewModel.conditionId;
            domainModel.name = conditionViewModel.name;
            domainModel.description = conditionViewModel.description;
        };

        var mapPlanRateViewToDomainModel = function(planRateViewModel) {
            var domainModel = {};

            domainModel.id = planRateViewModel.planRateId;
            domainModel.supplemental_life_insurance_plan = planRateViewModel.supplementalLifeInsurancePlanId;
            domainModel.age_min = planRateViewModel.ageMin;
            domainModel.age_max = planRateViewModel.ageMax;
            domainModel.bind_type = planRateViewModel.bindType;
            domainModel.rate = planRateViewModel.ratePer10000;
            domainModel.condition = planRateViewModel.planCondition.conditionId;

            return domainModel;
        };

        var mapPlanRateTableViewToDomainModel = function(planRateTableViewModel) {
            var domainModel = [];

            _.each(planRateTableViewModel.employeeRateTable, function(combinedRateViewModel)
                {
                    domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.tobaccoRate));
                    domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.nonTobaccoRate));
                });
            _.each(planRateTableViewModel.spouseRateTable, function(combinedRateViewModel)
                {
                    domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.tobaccoRate));
                    domainModel.push(mapPlanRateViewToDomainModel(combinedRateViewModel.nonTobaccoRate));
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
            ageRanges.push({"min": rateTableMaxAgeLimit, "max": -1});

            // Construct the rate table based on the inputs and the 
            // age ranges
            var rateTable = [];
            _.each(ageRanges, function(ageRange) {
                rateTable.push({
                    'ageMin' : ageRange.min,
                    'ageMax' : ageRange.max,
                    'bindType' : bindType,
                    'planCondition' : mapConditionDomainToViewModel(planCondition)
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
                        'ageMax' : -1,
                        'bindType' : 'dependent',
                        'planCondition' : mapConditionDomainToViewModel(conditions['Unknown'])
                    };

                deferred.resolve(viewModel);
            });

            return deferred.promise; 
        };

        var getAgeRangeForDisplay = function(rateViewModel) {
            if (rateViewModel.ageMin >= 0 && rateViewModel.ageMax >= 0){
                return rateViewModel.ageMin + ' through ' + rateViewModel.ageMax;
            } else if (rateViewModel.ageMin >= 0) {
                return rateViewModel.ageMin + ' and above';
            } else if (rateViewModel.ageMax >= 0) {
                return rateViewModel.ageMax + ' and under';
            } else {
                return 'All';
            }
        };

        //////////////////////////////////////////////////////////////////
        // End : Plan rate table helpers
        //////////////////////////////////////////////////////////////////

        // Testing Fake Data
        var plan = {
            "id": 1,
            "name": "Alibaba_Sup_Life",
            "supplemental_life_insurance_plan_rate": rateTable
        };

        var conditions = [
            {
                "id" : 1,
                "name" : "Default",
                "description": "default"
            },
            {
                "id" : 1,
                "name" : "Tobacco",
                "description": "tobacco"
            },
            {
                "id" : 2,
                "name" : "Non-Tobacco",
                "description": "non-tobacco"
            }
        ];

        var rateTable = [
            {
                "id": 1,
                "supplemental_life_insurance_plan" : 1,
                "age_min":null,
                "age_max":24,
                "bind_type":"self",
                "rate": 0.22,
                "condition": conditions[1]
            },
            {
                "id": 2,
                "supplemental_life_insurance_plan" : 1,
                "age_min":25,
                "age_max":29,
                "bind_type":"self",
                "rate": 0.33,
                "condition": conditions[1]
            },
            {
                "id": 3,
                "supplemental_life_insurance_plan" : 1,
                "age_min":30,
                "age_max":34,
                "bind_type":"self",
                "rate": 0.66,
                "condition": conditions[1]
            },
            {
                "id": 4,
                "supplemental_life_insurance_plan" : 1,
                "age_min":null,
                "age_max":24,
                "bind_type":"spouse",
                "rate": 1.22,
                "condition": conditions[2]
            },
            {
                "id": 5,
                "supplemental_life_insurance_plan" : 1,
                "age_min":25,
                "age_max":29,
                "bind_type":"spouse",
                "rate": 1.33,
                "condition": conditions[2]
            },
            {
                "id": 6,
                "supplemental_life_insurance_plan" : 1,
                "age_min":30,
                "age_max":34,
                "bind_type":"spouse",
                "rate": 1.66,
                "condition": conditions[2]
            },
            {
                "id": 7,
                "supplemental_life_insurance_plan" : 1,
                "age_min":null,
                "age_max":null,
                "bind_type":"dependent",
                "rate": 8.22,
                "condition": conditions[0]
            }
        ];

        var companyPlan = {
            "id" : 1,
            "supplemental_life_insurance_plan" : plan,
            "company" : 1,
            "created_at": "2015-05-05 20:09:42.496-04"
        };

        var beneficiaryList = [
            {
                "id" : 1,
                "first_name" : "aaa",
                "last_name" : "bbb",
                "relationship" : "friend",
                "email" : "abc@sdhadslj.com",
                "phone" : "1111111111",
                "percentage" : "22",
                "tier" : 1,
                "person_company_supplemental_life_insurance_plan" : "1"
            },
            {
                "id" : 2,
                "first_name" : "111",
                "last_name" : "222",
                "relationship" : "wahaha",
                "email" : "def@sdhadslj.com",
                "phone" : "2222222222",
                "percentage" : "77",
                "tier" : 2,
                "person_company_supplemental_life_insurance_plan" : "1"
            }
        ];

        var personCompanyPlan = {
            "id" : 1,
            "company_supplemental_life_insurance_plan" : companyPlan,
            "person" : 3,
            "self_elected_amount": 200000,
            "spouse_elected_amount": null,
            "child_elected_amount": 10000,
            "self_premium_per_month": 222,
            "spouse_premium_per_month" : 0,
            "child_premium_per_month" : 11,
            "self_condition": "tobacco",
            "spouse_condition": "non-tobacco",
            "life_insurance_beneficiary" : beneficiaryList
        };

        return {
            planBindTypes: ['self', 'spouse', 'dependent'],
            
            getPlansForCompany: function(companyId) {
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
            },

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

                    SupplementalLifeInsuranceRepository.CompanyPlanByCompany.save({companyId:companyId}, companyPlanDomainModel)
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

            getPlanByUser: function(userId) {
                var deferred = $q.defer();

                PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
                    SupplementalLifeInsuranceRepository.CompanyPersonPlanByPerson.query({personId:personInfo.id})
                    .$promise.then(function(personPlans) {
                        var plan = personPlans.length > 0 ?
                            mapPersonCompanyPlanDomainToViewModel(personPlans[0]) :
                            null;
                        deferred.resolve(plan);
                    },
                    function(error) {
                        deferred.reject(error);
                    });
                },
                function(error){
                    deferred.reject(error);
                });
                
                return deferred.promise; 
            }
        }; 
    }
]);
