var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitUpdateReasonService',
  ['$http',
   '$q',
   function($http, $q){
      var _benefitUpdateReasons = undefined;

      var mapReasonsToViewModels = function(domainReasons) {
        var viewCategories = [];
        _.each(domainReasons, function(domainReason) {
          var category = domainReason.category;

          if (category){
            var reason = {
              "id": domainReason.id,
              "name": domainReason.name,
              "description": domainReason.description,
              "detail_required": domainReason.detail_required
            };

            var existCategory = _.find(viewCategories, function(viewCategory){
              return viewCategory.id === category.id;
            });

            if (existCategory) {
              existCategory.reasons.push(reason);
            } else {
              category.reasons = [];
              category.reasons.push(reason);
              viewCategories.push(category);
            }
          }

        });

        return viewCategories;
      };

      var getAllReasons = function(){
         var deferred = $q.defer();

         if(!_benefitUpdateReasons){
            $http.get('/api/v1/benefit_update_reasons/').success(function(data){
               _benefitUpdateReasons = mapReasonsToViewModels(data);
               deferred.resolve(_benefitUpdateReasons);
            }).error(function(data){
               deferred.reject(data);
            });
         }
         else{
            deferred.resolve(_benefitUpdateReasons);
         }
         return deferred.promise;
      }; 

      var getReasonByName = function(reasonName) {
          return getAllReasons().then(
            function(allReasons) {
                return _(allReasons)
                    .chain()
                    .pluck('reasons')
                    .flatten()
                    .find(function(reason) { 
                        return reason.name.trim().toLowerCase() === reasonName.trim().toLowerCase(); 
                    })
                    .value();
            }
          );
      };

      var getNewHireReason = function() {
          return getReasonByName('new hire');
      };

      return{
         getAllReasons: getAllReasons,
         getReasonByName: getReasonByName,
         getNewHireReason : getNewHireReason
      }
   }
]);
