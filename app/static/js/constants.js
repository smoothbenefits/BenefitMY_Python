var settings = angular.module('benefitmyApp.constants',[]);

settings.constant('profileSettings', [
    {
        name: 'i9',
        display_name: 'I-9',
        valid_fields: [
            {
                name: 'worker_type',
                display_name: 'Worker Type',
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
                datamap: [['0', 'Single'], ['1', 'Married'], ['2', 'Married, but withold at higher Single rate']],
                id: 3
            },
            {
                name: 'tax_credit',
                display_name: 'At least $1900 for tax credit as child or dependent care expenses',
                datamap: [['0', 'No'], ['1', 'Yes']],
                id: 4
            },
            {
                name: 'total_points',
                display_name: 'Total points',
                id: 5
            }
        ]
    }
]);
