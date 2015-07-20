var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'CompanyFeatureService',
   ['$q', 'CompanyFeatureRepository',
   function($q, CompanyFeatureRepository){

      var mapToViewModel = function(dataModel) {
         var viewModel = {
            company: dataModel.company,
            companyFeatureId: dataModel.company_feature.id,
            companyFeatureName: dataModel.company_feature.feature,
            enabled: dataModel.feature_status
         };

         return viewModel;
      };

      var getDisabledCompanyFeatureByCompany = function(companyId) {
         var deferred = $q.defer();

         CompanyFeatureRepository.CompanyFeatureByCompany.query({companyId: companyId}).$promise.then(function(response){
            var companyFeatures = [];
            _.each(response, function(feature) {
               var viewModel = mapToViewModel(feature);
               companyFeatures.push(viewModel);
            });

            var hashTable = {};
            _.each(companyFeatures, function(feature) {
               hashTable[feature.companyFeatureName] = !feature.enabled;
            });

            deferred.resolve(hashTable);
         }, function(error) {
            deferred.reject(error);
         });

         return deferred.promise;
      };

      return{
         getDisabledCompanyFeatureByCompany: getDisabledCompanyFeatureByCompany
      };
   }
]);
