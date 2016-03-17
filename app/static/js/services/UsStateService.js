var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UsStateService',
    [
        '$http',
        'UsStateRepository',
        function($http,
                 UsStateRepository){
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
                if(!searchTerm){
                    searchTerm = '';
                }
                return UsStateRepository.get({text:searchTerm})
                    .$promise.then(function(resp){
                        return resp.RestResponse.result.map(function(item){
                            return item.name;
                          });
                    }, function(error){
                        return getMemoryStates(searchTerm);
                    });
            };

            var GetAllStates = function(){
                return UsStateRepository.get()
                    .$promise.then(function(resp){
                        return resp.RestResponse.result.map(function(item){
                            return item.name;
                          });
                    }, function(error){
                        return states;
                    });
            }

            return {
                GetStates: GetStates
            };
        }
    ]
);
