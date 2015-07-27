var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitElectionService',
  ['companyEmployeeBenefits', '$q',
  function(companyEmployeeBenefits, $q){

    var getBenefitElectionsByCompany = function(companyId){
      var deferred = $q.defer();
        companyEmployeeBenefits.selected.get({companyId: companyId})
        .$promise.then(function(response){
          var selectedBenefits = response.benefits;

          var benefitElectedArray = [];
          _.each(selectedBenefits, function(benefit){
            var displayBenefit = { enrolled: [] };
            displayBenefit.selectedPlanName = benefit.benefit.benefit_plan.name;
            displayBenefit.selectedPlanType = benefit.benefit.benefit_option_type;
            displayBenefit.lastUpdatedTime = moment(benefit.updated_at).format(DATE_FORMAT_STRING);
            displayBenefit.pcp = benefit.pcp;
            _.each(benefit.enrolleds, function(enrolled){
              if (enrolled.person.relationship === 'self'){
                displayBenefit.userId = enrolled.person.user;
                displayBenefit.name = enrolled.person.first_name + ' ' + enrolled.person.last_name;
                displayBenefit.email = enrolled.person.email;
              }
              var displayEnrolled = { name: enrolled.person.first_name + ' ' + enrolled.person.last_name, relationship: enrolled.person.relationship, pcp:enrolled.pcp};
              displayBenefit.enrolled.push(displayEnrolled);
            });

            benefitElectedArray.push(displayBenefit);
          });
          deferred.resolve(benefitElectedArray);
        }, function(failedResponse){
          deferred.reject(failedResponse);
        });
        return deferred.promise;
    };

    var getBenefitWaivedListByCompany = function(companyId){
      var deferred = $q.defer();
      benefitWaivedList = [];
      companyEmployeeBenefits.waived.query({companyId: companyId})
      .$promise.then(function(waivedResponse){
        _.each(waivedResponse, function(waived){
          benefitWaivedList.push({
            lastUpdatedTime:moment(waived.created_at).format(DATE_FORMAT_STRING),
            userId: waived.user.id,
            email: waived.user.email,
            benefitType: waived.benefit_type,
            reason: waived.reason
          });
        });
        deferred.resolve(benefitWaivedList);
      });
      return deferred.promise;
    };


    return{
      getBenefitElectionsByCompany: getBenefitElectionsByCompany,
      getBenefitWaivedListByCompany: getBenefitWaivedListByCompany
    };
}]);
