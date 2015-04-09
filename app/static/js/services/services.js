var benefitmyService = angular.module('benefitmyService', ['benefitmyDomainModelFactories']);

var utilityService = benefitmyService.factory('utilityServcie', 
  ['$q',
   'profileSettings',
    function($q,
             profileSettings){
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

      return {
        mapObjectToKeyPairArray: mapObjectToKeyPairArray
      };
    }
  ]);