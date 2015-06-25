var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BrowserDetectionService', 
    [function () {

    	// Use Regex to fetch major browsers and their version number
    	// A better way to do is to detect rendering engine or directly 
    	// detect features that we need the browser to support. 
    	// We might want to know more about the concept polyfill later if
    	// we decide to support older version of browsers.
        var getCurrentBrowser = function () {
            var ua = navigator.userAgent, tem;
            M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
            if (/trident/i.test(M[1])) {
                tem =  /\brv[ :]+(\d+)/g.exec(ua) || [];
                return 'IE '+(tem[1] || '');
            }
            if (M[1] === 'Chrome'){
                tem = ua.match(/\b(OPR|Edge)\/(\d+)/);
                if (tem!= null) {
                	return tem.slice(1).join(' ').replace('OPR', 'Opera');
                }
            }
            M = M[2] ? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
            if ((tem = ua.match(/version\/(\d+)/i))!= null) {
            	M.splice(1, 1, tem[1]);
            }
            return M.join(' ');
        };

        return {
        	getCurrentBrowser : getCurrentBrowser
        };
    }
]);