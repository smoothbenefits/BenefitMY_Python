var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitSummaryService',
  ['$q',
  'PersonService',
  'PersonBenefitEnrollmentRepository',
  'CompanyBenefitAvailabilityService',
  function BenefitSummaryService(
    $q,
    PersonService,
    PersonBenefitEnrollmentRepository,
    CompanyBenefitAvailabilityService){

    var SELECTED = 'SELECTED';
    var NOT_SELECTED = 'NOT_SELECTED';
    var WAIVED = 'WAIVED';

    var mapPersonBenefitToViewModel = function (domainModel) {
      var viewModel = {};

      // Map enrolled health benefits
      if (domainModel.health_benefit_enrolled[0] != null) {
        _.each(domainModel.health_benefit_enrolled, function(enrolled) {
          var benefitType = enrolled.benefit.benefit_plan.benefit_type.name.toLowerCase();
          var viewEnrolled = {
            "plan_name": enrolled.benefit.benefit_plan.name,
            "option_type": enrolled.benefit.benefit_option_type,
            "status": SELECTED
          };
          viewModel[benefitType] = viewEnrolled;
        });
      }

      // Map waived health benefits
      if (domainModel.health_benefit_waived[0] != null) {
        _.each(domainModel.health_benefit_waived, function(waived) {
          var benefitType = waived.benefit_type.name.toLowerCase();
          var viewWaived = {
            "status": WAIVED,
            "reason": waived.reason,
            "plan_name": "Not Applicable",
            "option_type": "Not Applicable"
          };
          viewModel[benefitType] = viewWaived;
        });
      }

      // Map HRA plan enrollment
      if (domainModel.hra[0] != null) {
        var domainHra = domainModel.hra[0];
        viewModel['hra'] = {
          "plan_name": domainHra.company_hra_plan.hra_plan.name,
          "description": domainHra.company_hra_plan.hra_plan.description
        };
      }

      // Map basic life insurance enrollment
      if (domainModel.basic_life[0] != null) {
        var domainBasicLife = domainModel.basic_life[0];

        if (domainBasicLife.company_life_insurance) {
          viewModel['basic_life'] = {
            "plan_name": domainBasicLife.company_life_insurance.life_insurance_plan.name,
            "beneficiary": domainBasicLife.life_insurance_beneficiary,
            "status": SELECTED
          };
        } else {
          viewModel['basic_life'] = {
            "status": WAIVED
          };
        }
      }

      // Map supplemental life insurance enrollment
      if (domainModel.supplemental_life[0] != null) {
        var domainSupplementalLife = domainModel.supplemental_life[0];
        viewModel['supplemental_life'] = {
          "plan_name": domainSupplementalLife.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name,
          "beneficiary": domainSupplementalLife.suppl_life_insurance_beneficiary,
          "self_elected_amount": domainSupplementalLife.self_elected_amount,
          "spouse_elected_amount": domainSupplementalLife.spouse_elected_amount,
          "child_elected_amount": domainSupplementalLife.child_elected_amount,
          "self_condition": domainSupplementalLife.self_condition.name,
          "spouse_condition": domainSupplementalLife.spouse_condition.name
        };
      }

      // Map STD enrollment
      if (domainModel.std[0] != null) {
        var domainStd = domainModel.std[0];
        viewModel['std'] = {
          "plan_name": domainStd.company_std_insurance.std_insurance_plan.name,
          "percentage_of_salary": domainStd.company_std_insurance.percentage_of_salary,
          "max_benefit_weekly": domainStd.company_std_insurance.max_benefit_weekly,
          "duration": domainStd.company_std_insurance.duration,
          "rate": domainStd.company_std_insurance.rate,
          "employer_contribution_percentage": domainStd.company_std_insurance.employer_contribution_percentage,
          "elimination_period_in_days": domainStd.company_std_insurance.elimination_period_in_days
        };
      }

      // Map LTD enrollment
      if (domainModel.ltd[0] != null) {
        var domainLtd = domainModel.ltd[0];
        viewModel['ltd'] = {
          "plan_name": domainLtd.company_ltd_insurance.ltd_insurance_plan.name,
          "percentage_of_salary": domainLtd.company_ltd_insurance.percentage_of_salary,
          "max_benefit_monthly": domainLtd.company_ltd_insurance.max_benefit_monthly,
          "duration": domainLtd.company_ltd_insurance.duration,
          "rate": domainLtd.company_ltd_insurance.rate,
          "employer_contribution_percentage": domainLtd.company_ltd_insurance.employer_contribution_percentage,
          "elimination_period_in_months": domainLtd.company_ltd_insurance.elimination_period_in_months
        };
      }

      // Map FSA selection
      if (domainModel.fsa[0] != null) {
        var domainFsa = domainModel.fsa[0];
        viewModel['fsa'] = {
          "primary_amount_per_year": domainFsa.primary_amount_per_year,
          "dependent_amount_per_year": domainFsa.dependent_amount_per_year,
          "update_reason": domainFsa.update_reason
        };
        if (domainFsa.company_fsa_plan){
          viewModel['fsa'].status = SELECTED;
        } else {
          viewModel['fsa'].status = WAIVED;
        }
      }

      return viewModel;
    };

    var getBenefitEnrollmentByUser = function(userId, companyId) {
      var deferred = $q.defer();

      PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
        return personInfo.id;
      }).then(function(personId) {
        var enrolled = PersonBenefitEnrollmentRepository.BenefitEnrollmentByPerson.get({personId: personId})
        .$promise.then(function(enrollments) {
          var viewPersonBenefits = mapPersonBenefitToViewModel(enrollments);
          return viewPersonBenefits;
        });
        return enrolled;
      }).then(function(personEnrollment) {
        CompanyBenefitAvailabilityService.getBenefitAvailabilityByCompany(companyId)
        .then(function(companyBenefits) {
          // First, get all benefits that the company offers
          var companyBenefitHash = _.pairs(companyBenefits);
          var offeredBenefits = _.filter(companyBenefitHash, function(keyValue){
            return keyValue[1];
          });

          // Loop through offered benefits and fill in any unselected gap
          _.each(offeredBenefits, function(companyBenefitKeyValue) {
            var offeredBenefitType = companyBenefitKeyValue[0];

            if (!personEnrollment[offeredBenefitType]) {
              personEnrollment[offeredBenefitType] = {
                "status": NOT_SELECTED
              };
            } else if (!personEnrollment[offeredBenefitType].status) {
              personEnrollment[offeredBenefitType].status = SELECTED;
            }
          });

          deferred.resolve(personEnrollment);
        });
      }).catch(function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    return{
      getBenefitEnrollmentByUser: getBenefitEnrollmentByUser
    };
}]);
