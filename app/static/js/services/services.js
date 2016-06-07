var benefitmyService = angular.module('benefitmyService', ['benefitmyDomainModelFactories']);

var utilityService = benefitmyService.factory('utilityService',
  ['$q',
   'profileSettings',
   'envService',
    function($q,
             profileSettings,
             envService){
      var mapObjectToKeyPairArray = function(type, object){
        var fields = [];

        var pairs = _.pairs(object);
        var validFields = _.findWhere(profileSettings, {name: type}).valid_fields;
        _.each(pairs, function(pair){
          var key = pair[0];
          var inSetting = _.findWhere(validFields, {name: key});
          if (inSetting){
            if (inSetting.datamap){
              var value = pair[1];
              var mappedValue = _.find(inSetting.datamap, function(map){
                return map[0] === value.toString();
              });
              if (!mappedValue){
                inSetting.value = 'UNKNOWN';
              } else{
                inSetting.value = mappedValue[1];
              }
            } else{
              inSetting.value = pair[1];
            }
            fields.push(inSetting);
          }
        });

        return fields;
      };

      /**
        Get a descriptor of the given ID based on the environment
        of the context.
      */
      var getEnvAwareId = function(id){
            var env = envService.get();
            return env + '_' + id;
      };

      var retrieveIdFromEnvAwareId = function(envAwareId){
        var breakIndex = envAwareId.indexOf('_');
        var id = envAwareId.substring(breakIndex + 1);
        return id;
      };

      var normalizeLink = function(originalLink){
            if (!originalLink || !originalLink.trim()) {
                return originalLink;
            }

            var resultLink = originalLink;
            if(!(resultLink.toLowerCase().indexOf('http://') == 0) 
                && !(resultLink.toLowerCase().indexOf('https://') == 0)) {
              resultLink = 'http://' + resultLink;
            }
            return resultLink;
        }

      return {
        mapObjectToKeyPairArray: mapObjectToKeyPairArray,
        getEnvAwareId: getEnvAwareId,
        retrieveIdFromEnvAwareId: retrieveIdFromEnvAwareId,
        normalizeLink: normalizeLink
      };
    }
  ]);
