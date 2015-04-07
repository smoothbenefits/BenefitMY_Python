var settings = angular.module('benefitmyApp.constants',[]);

settings.constant('profileSettings', [
    {
        name: 'i9',
        display_name: 'I-9',
        valid_fields: [
            {
                name: 'worker_type',
                display_name: 'Worker Type',
                datamap: [['Aaw', 'Alien authorized to work'], ['PResident', 'Permanent resident'], ['Noncitizen', 'Noncitizen national of the United States'], ['Citizen', 'Citizen of the United States']],
                id: 1
            },
            {
                name: 'uscis_number',
                display_name: 'USCIS Number',
                id: 2
            },
            {
                name: 'expiration_date',
                display_name: 'Expiration Date',
                id: 3
            },
            {
                name: 'i_94',
                display_name: 'I-94 Admission Number',
                id: 4
            },
            {
                name: 'passport',
                display_name: 'Passport Number',
                id: 5
            },
            {
                name: 'country',
                display_name: 'Country',
                id: 6
            }
        ],
    },
    {
        name: 'w4',
        display_name: 'W-4',
        valid_fields: [
            {
                name: 'dependencies',
                display_name: 'Number of dependencies',
                id: 1
            },
            {
                name: 'head',
                display_name: 'Head of household',
                datamap: [['0', 'No'], ['1', 'Yes']],
                id: 2
            },
            {
                name: 'marriage',
                display_name: 'Withhold type',
                datamap: [['0', 'Single'], ['2', 'Married'], ['1', 'Married, but withold at higher Single rate']],
                id: 3
            },
            {
                name: 'tax_credit',
                display_name: 'At least $1900 for tax credit as child or dependent care expenses',
                datamap: [['0', 'No'], ['1', 'Yes']],
                id: 4
            },
            {
                name: 'calculated_points',
                display_name: 'Calculated withhold number (based on your dependents and withold type)',
                id: 5
            },
            {
                name: 'user_defined_points',
                display_name: 'W-4 paycheck withhold number',
                id: 6
            },
            {
                name: 'extra_amount',
                display_name: 'Extra amount to withhold annually from paycheck for Tax',
                id: 7
            }
        ]
    }
]);

settings.constant('benefitSectionGlobalConfig', [
    {
        id: 1,
        section_name: 'supplemental_life_insurance',
        enabled: false
    }
]);

settings.constant('tabLayoutGlobalConfig', [
    {
        id: 1,
        section_name: 'broker_add_benefits',
        tabs: [
            {
                id: 1,
                verbose_name: "Health Benefits",
                name: "health",
                active: true,
                state: "broker_add_benefit.health"
            },
            {
                id: 1,
                verbose_name: "Basic Life Insurance",
                name: "basic_life",
                active: false,
                state: "broker_add_benefit.basic_life_insurance"
            }
        ]
    },
    {
        id: 2,
        section_name: 'employee_profile',
        tabs: [
            {
                id: 1,
                verbose_name: 'I-9',
                name: 'i9',
                active: false,
                state: 'employee_profile.i9'
            },
            {
                id: 2, 
                verbose_name: 'W-4',
                name: 'w4',
                active: false,
                state: 'employee_profile.w4'
            }
        ]
    },
    {
        id: 3,
        section_name: 'employee_payroll',
        tabs: [
            {
                id: 1,
                verbose_name: 'W4 Form',
                name: 'w4',
                active: true,
                state: 'employee_payroll.w4'
            },
            {
                id: 2,
                verbose_name: 'Direct Deposit',
                name: 'direct_deposit',
                active: false,
                state: 'employee_payroll.direct_deposit'
            }
        ]
    }
]);
