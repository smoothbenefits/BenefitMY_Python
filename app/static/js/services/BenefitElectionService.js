var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitElectionService', 
  ['companyEmployeeBenefits',
  function(companyEmployeeBenefits){
    return{
      getBenefitElectionsByCompany: function(companyId, success, failed){
        companyEmployeeBenefits.selected.get({companyId: companyId})
          .$promise.then(function(response){
            var selectedBenefits = response.benefits;

            var benefitElectedArray = [];
            _.each(selectedBenefits, function(benefit){
              var displayBenefit = { enrolled: [] };

              _.each(benefit.enrolleds, function(enrolled){
                if (enrolled.person.relationship === 'self'){
                  displayBenefit.userId = enrolled.person.user;
                  displayBenefit.name = enrolled.person.first_name + ' ' + enrolled.person.last_name;
                  displayBenefit.email = enrolled.person.email;
                }
                var displayEnrolled = { name: enrolled.person.first_name + ' ' + enrolled.person.last_name, relationship: enrolled.person.relationship};
                displayBenefit.enrolled.push(displayEnrolled);
              });

              displayBenefit.selectedPlanName = benefit.benefit.benefit_plan.name;
              displayBenefit.selectedPlanType = benefit.benefit.benefit_option_type;
              displayBenefit.lastUpdatedTime = moment(benefit.updated_at).format(DATE_FORMAT_STRING);
              displayBenefit.pcp = benefit.pcp;

              benefitElectedArray.push(displayBenefit);
            });

          //Now working on the waived list
          companyEmployeeBenefits.waived.query({companyId: companyId})
            .$promise.then(function(waivedResponse){
              _.each(waivedResponse, function(waived){
                selectedBenefit = _.find(benefitElectedArray, function(displayBenefit){
                  return displayBenefit.userId === waived.user.id;
                });
                if(selectedBenefit){
                  if(!selectedBenefit.waivedList){
                    selectedBenefit.waivedList = [];
                  }
                  selectedBenefit.waivedList.push(waived.benefit_type.name);
                  selectedBenefit.updated = moment(waived.created_at).format(DATE_FORMAT_STRING);
                }
                else{
                  selectedBenefit = {waivedList:[], updated:moment(waived.created_at).format(DATE_FORMAT_STRING)};
                  selectedBenefit.waivedList.push(waived.benefit_type.name);
                  benefitElectedArray.push(selectedBenefit);
                }
              });
            if(success){
              success(benefitElectedArray);
            }  
          }, function(failedResponse){
            if(failed){
              failed(failedResponse);
            }
          });
        }, function(failedResponse){
            if(failed){
              failed(failedResponse);
            }
        });
        
      },
     getBenefitElectionsByBroker: function(broker_user_id){

     }
    };
      
}]);
