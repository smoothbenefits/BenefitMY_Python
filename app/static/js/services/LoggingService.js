var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LoggingService', 
  ['$window',
   '$log',
   '$timeout',
   '$q',
   'BrowserDetectionService',
  function ($window, $log, $timeout, $q, BrowserDetectionService){
    var sendLog = function(logType, message, customData){
        $q(function() {
            // Logging should be considered non-critical operation
            // can should not be blocking at all
            // So if something bad happens during logging, simply
            // log the issue to console, and swallow the exception
            try {

                // use our traceService to generate a stack trace 
                var stackTrace = printStackTrace(); 

                // use AJAX (in this example jQuery) and NOT 
                // an angular service such as $http 
                $.ajax({ 
                    type: "POST", 
                    url: LOGGING_SERVER_URL, 
                    contentType: "application/json", 
                    data: angular.toJson({ 
                        url: $window.location.href, 
                        message: message,
                        browser: BrowserDetectionService.getBrowserBrand(), 
                        type: logType, 
                        customData: customData,
                        stackTrace: stackTrace.join('\n\n')}) })
                .fail(function(jqXHR, textStatus, errorThrown) {
                    $log.warn("Error server-side logging failed");
                    $log.log(errorThrown);
                }); 

            } catch (loggingError) {
                $log.warn("Error server-side logging failed"); 
                $log.log(loggingError);
            }    
        });
    };
    return {
      error: function(message, customData) {
        sendLog('error', message, customData);
      },
      warning: function(message, customData) {
        sendLog('warning', message, customData);
      },
      info: function(message, customData) {
        sendLog('info', message, customData);
      },
      debug: function(message, customData) {
        sendLog('debug', message, customData);
      }
    };
}]);
