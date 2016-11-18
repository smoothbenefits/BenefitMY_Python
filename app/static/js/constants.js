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
                id: 2,
                verbose_name: "HRA",
                name: "hra",
                active: false,
                state: "broker_add_benefit.hra"
            },
            {
                id: 3,
                verbose_name: "Basic Life Insurance (AD&D)",
                name: "basic_life",
                active: false,
                state: "broker_add_benefit.basic_life_insurance"
            },
            {
                id: 4,
                verbose_name: "Suppl. Life Insurance",
                name: "supplemental_life",
                active: false,
                state: "broker_add_benefit.supplemental_life_insurance"
            },
            {
                id: 5,
                verbose_name: "STD",
                name: "std",
                active: false,
                state: "broker_add_benefit.std"
            },
            {
                id: 6,
                verbose_name: "LTD",
                name: "ltd",
                active: false,
                state: "broker_add_benefit.ltd"
            },
            {
                id: 7,
                verbose_name: "HSA",
                name: "hsa",
                active: false,
                state: "broker_add_benefit.hsa"
            },
            {
                id: 8,
                verbose_name: "FSA",
                name: "fsa",
                active: false,
                state: "broker_add_benefit.fsa"
            },
            {
                id: 9,
                verbose_name: "Commuter",
                name: "commuter",
                active: false,
                state: "broker_add_benefit.commuter"
            },
            {
                id: 10,
                verbose_name: "Extra Benefits",
                name: "extra_benefit",
                active: false,
                state: "broker_add_benefit.extra_benefit"
            },
        ]
    },
    {
        id: 2,
        section_name: 'employee_profile',
        tabs: [
            {
                id: 1,
                verbose_name: 'Employment Authorization (I9)',
                name: 'i9',
                active: true,
                state: 'employee_profile.i9'
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
                active: false,
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
    },
    {
        id: 4,
        section_name: 'employee_onboard',
        tabs: [
            {
                id: 1,
                verbose_name: 'Basic Information',
                description: 'Personal information',
                name: 'basic_info',
                active: true,
                state: 'employee_onboard.basic_info'
            },
            {
                id: 2,
                verbose_name: 'Employment Authorization',
                description: 'Employment and proof of eligibility',
                name: 'employment',
                active: false,
                state: 'employee_onboard.employment'
            },
            {
                id: 3,
                verbose_name: 'Tax information (W-4)',
                description: 'Information about your W-4 and state tax withholding form',
                name: 'tax',
                active: false,
                state: 'employee_onboard.tax'
            },
            {
                id: 4,
                verbose_name: 'Direct Deposit Information',
                description: 'Information about your direct deposit accounts setup',
                name: 'direct_deposit',
                active: false,
                state: 'employee_onboard.direct_deposit'
            },
            {
                id: 5,
                verbose_name: 'Employee Documents',
                description: 'Documents required by the employer',
                name: 'document',
                active: false,
                state: 'employee_onboard.document'
            }
        ]
    }
]);

settings.constant('EmploymentStatuses',{
    active: 'Active',
    prospective: 'Prospective',
    terminated: 'Terminated',
    onLeave:'OnLeave'
});

settings.constant('MonthsInYear',[
    {
        id: 0,
        name: moment().month(0).format("MMMM")
    },
    {
        id: 1,
        name: moment().month(1).format("MMMM")
    },
    {
        id: 2,
        name: moment().month(2).format("MMMM")
    },
    {
        id: 3,
        name: moment().month(3).format("MMMM")
    },
    {
        id: 4,
        name: moment().month(4).format("MMMM")
    },
    {
        id: 5,
        name: moment().month(5).format("MMMM")
    },
    {
        id: 6,
        name: moment().month(6).format("MMMM")
    },
    {
        id: 7,
        name: moment().month(7).format("MMMM")
    },
    {
        id: 8,
        name: moment().month(8).format("MMMM")
    },
    {
        id: 9,
        name: moment().month(9).format("MMMM")
    },
    {
        id: 10,
        name: moment().month(10).format("MMMM")
    },
    {
        id: 11,
        name: moment().month(11).format("MMMM")
    }
])
