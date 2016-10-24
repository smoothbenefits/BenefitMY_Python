var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'CompanyFeatureService',
   ['$q', 'CompanyFeatureRepository',
   function($q, CompanyFeatureRepository){

      var appFeatureStatusByCompanyIdCache = {};

      var AppFeatureNames = {
        FSA: 'FSA',
        DD: 'DD',
        MedicalBenefit: 'MedicalBenefit',
        DentalBenefit: 'DentalBenefit',
        VisionBenefit: 'VisionBenefit',
        I9: 'I9',
        Manager: 'Manager',
        BasicLife: 'BasicLife',
        OptionalLife: 'OptionalLife',
        STD: 'STD',
        LTD: 'LTD',
        HRA: 'HRA',
        W4: 'W4',
        ADAD: 'ADAD',
        BenefitsForFullTimeOnly: 'BenefitsForFullTimeOnly',
        Commuter: 'Commuter',
        ExtraBenefit: 'ExtraBenefit',
        Timeoff: 'Timeoff',
        WorkTimeSheet: 'WorkTimeSheet',
        WorkTimeSheetNotification: 'WorkTimeSheetNotification',
        RangedTimeCard: 'RangedTimeCard',
        ProjectManagement: 'ProjectManagement',
        MobileProjectManagement: 'MobileProjectManagement',
        ShowDisabledFeaturesForEmployer: 'ShowDisabledFeaturesForEmployer'
      };

      var getAllApplicationFeatureStatusByCompany = function(companyId) {
        var deferred = $q.defer();

        if (appFeatureStatusByCompanyIdCache[companyId]) {
            deferred.resolve(appFeatureStatusByCompanyIdCache[companyId]);
        } else {
            CompanyFeatureRepository.AllApplicationFeatureStatusByCompany.query({companyId: companyId})
            .$promise.then({
                function(appFeatureStatus) {
                    // Attach the needed utility method onto the object
                    appFeatureStatus.isFeatureEnabled = function(appFeatureName) {
                        if (appFeatureName in this) {
                            return this[appFeatureName];
                        }
                        // This should not happen if all features have been properly
                        // spelled out on the server side, but just in case, assume
                        // the feature is on if server does not spell for it
                        return true;
                    };
                    deferred.resolve(appFeatureStatus);
                },
                function(errors) {
                    deferred.reject(errors);
                }
            });
        }

        return deferred.promise;
      };

      return{
         AppFeatureNames: AppFeatureNames,
         getAllApplicationFeatureStatusByCompany: getAllApplicationFeatureStatusByCompany
      };
   }
]);
