var benefitmyService = angular.module('benefitmyService');

/**
    A service to help detecting the user browser (and version) info.
*/
benefitmyService.service('BrowserDetectionService', 
    ['$window', function($window) {

     return {

        /**
            Get the brand name of the browser. 
        */
        getBrowserBrand : function() {

            // TODO:
            // This is only a very crude implementation, but it is
            // mostly accurate, and can identify the 4 main stream
            // browsers being used in markets quite accurately.
            var userAgent = $window.navigator.userAgent;

            var browsers = {chrome: /chrome/i, safari: /safari/i, firefox: /firefox/i, ie: /internet explorer/i};

            for(var key in browsers) {
                if (browsers[key].test(userAgent)) {
                    return key;
                }
            };

           return 'unknown';
        }
    };

}]);