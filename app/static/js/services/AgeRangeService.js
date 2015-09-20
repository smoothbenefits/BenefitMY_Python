var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('AgeRangeService',
    [
    function (){
        return function(ageStart, ageEnd, ageInteval, ageRangeMax){
            // Constants
            // Assumption: rateTableMinAgeLimit + N * rateTableAgeInterval = rateTableMaxAgeLimit
            //             i.e. no "fractions" at the end.
            var rateTableMinAgeLimit = ageStart;
            var rateTableMaxAgeLimit = ageEnd;
            var rateTableAgeInterval = ageInteval;

            // An artificial age max limit to support the notion of
            // 'X age and above'.
            var ageRangeMax = ageRangeMax;

            var getAgeRangeList = function(){
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

                return ageRanges;
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

            return {
                getAgeRangeList: getAgeRangeList,
                getAgeRangeForDisplay: getAgeRangeForDisplay,
                maxAge: rateTableMaxAgeLimit,
                minAge: rateTableMinAgeLimit
            };
        }
    }
]);