var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('FeatureConfigurationService',
  [ 'benefitSectionGlobalConfig',
    function(benefitSectionGlobalConfig){

    return {
      isFeatureOnForCompany : function(company_id, feature_id) {

        // Note that this is for now to provide the stub for the connonical place where
        // we should implement the feature configuration on our side.
        // When we have the feature-company configuration facility in place,
        // This should be the choke point and only place to talk to server side
        // to find out the data, and should be the only thing being referenced 
        // on the front-end for such information.
        var config = _.find(benefitSectionGlobalConfig, {section_name: feature_id});

        if (!config) {
            // Default to ture if no specific configuration specified
            return true;
        }

        return config.enabled;
      }
    };
  }
]);