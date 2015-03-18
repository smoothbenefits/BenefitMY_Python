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
