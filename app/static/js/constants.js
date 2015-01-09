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
        valid_fields: [
            {
                name:''
            }
        ]
    }
]);
