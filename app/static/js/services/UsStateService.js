var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UsStateService', [ function(){
            var states = [
                'Alabama',
                'Alaska',
                'Arizona',
                'Arkansas',
                'California',
                'Colorado',
                'Connecticut',
                'Delaware',
                'Florida',
                'Georgia',
                'Hawaii',
                'Idaho',
                'Illinois',
                'Indiana',
                'Iowa',
                'Kansas',
                'Kentucky',
                'Louisiana',
                'Maine',
                'Maryland',
                'Massachusetts',
                'Michigan',
                'Minnesota',
                'Mississippi',
                'Missouri',
                'Montana',
                'Nebraska',
                'Nevada',
                'New Hampshire',
                'New Jersey',
                'New Mexico',
                'New York',
                'North Dakota',
                'North Carolina',
                'Ohio',
                'Oklahoma',
                'Oregon',
                'Pennsylvania',
                'Rhode Island',
                'South Carolina',
                'South Dakota',
                'Tennessee',
                'Texas',
                'Utah',
                'Vermont',
                'Virginia',
                'Washington',
                'West Virginia',
                'Wisconsin',
                'Wyoming'
            ];

            var getMemoryStates = function(searchTerm){
                var matchedStates = [];
                _.each(states, function(stateItem){
                    if(stateItem.toLowerCase().indexOf(searchTerm) >= 0){
                        matchedStates.push(stateItem);
                    }
                });
                return matchedStates;
            };


            var GetStates = function(searchTerm){
                return getMemoryStates(searchTerm);
            };

            var GetAllStates = function(){
                return states;
            }

            return {
                GetStates: GetStates,
                GetAllStates: GetAllStates
            };
        }
    ]
);
