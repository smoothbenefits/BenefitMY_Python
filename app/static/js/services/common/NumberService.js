var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('NumberService',
  ['$q',
   function NumberService(
    $q){

        /**
            Convert the original number to a new value, such that
            the number of decimals is limited to the given value. 
            If the original value does not have more than numPlaces 
            decimal places, then the original value is returned 
            E.g. if numPlaces is given '2', then
              * 1 => 1
              * 1.2 => 1.2
              * 1.23 => 1.23
              * 1.234 => 1.23
        */
        var ToLimitDecimals = function(originalValue, numPlaces) {
            numPlaces = numPlaces ? numPlaces : 0;

            var numDecimals = _countDecimal(originalValue);
            if (numDecimals <= numPlaces) {
                return originalValue;
            }
            return originalValue.toFixed(numPlaces);    
        };

        var _countDecimal = function (number) {
            if(Math.floor(number) === number) {
                return 0;
            }
            return number.toString().split(".")[1].length || 0; 
        };

        return {
            ToLimitDecimals: ToLimitDecimals
        };
    }
]);
