var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('BenefitSummaryService',
  ['$q',
  'PersonService',
  'PersonBenefitEnrollmentRepository',
  function BenefitSummaryService(
    $q,
    PersonService,
    PersonBenefitEnrollmentRepository){

    var mapPersonBenefitToViewModel = function (domainModel) {
      var viewModel = {};

      // Map enrolled health benefits
      if (domainModel.health_benefit_enrolled[0] != null) {
        viewModel.health_benefit_enrolled = [];
        _.each(domainModel.health_benefit_enrolled, function(enrolled) {
          var viewEnrolled = {
            "plan_name": enrolled.benefit.benefit_plan.name,
            "benefit_type": enrolled.benefit.benefit_plan.benefit_type.name,
            "enrolled_member": enrolled.enrolleds
          };
          viewModel.health_benefit_enrolled.push(viewEnrolled);
        });
      } else {
        viewModel.health_benefit_enrolled = undefined;
      }

      // Map waived health benefits
      if (domainModel.health_benefit_waived[0] != null) {
        viewModel.health_benefit_waived = [];
        _.each(domainModel.health_benefit_waived, function(waived) {
          var viewWaived = {
            "benefit_type": waived.benefit_type.name,
            "reason": waived.reason
          };
          viewModel.health_benefit_waived.push(viewWaived);
        });
      } else {
        viewModel.health_benefit_waived = undefined;
      }

      // Map HRA plan enrollment
      if (domainModel.hra[0] != null) {
        var domainHra = domainModel.hra[0];
        viewModel.hra = {
          "plan_name": domainHra.company_hra_plan.hra_plan.name,
          "description": domainHra.company_hra_plan.hra_plan.description
        };
      } else {
        viewModel.hra = undefined;
      }

      // Map basic life insurance enrollment
      if (domainModel.basic_life[0] != null) {
        var domainBasicLife = domainModel.basic_life[0];
        viewModel.basic_life = {
          "plan_name": domainBasicLife.company_life_insurance.life_insurance_plan.name,
          "beneficiary": domainBasicLife.life_insurance_beneficiary
        };
      } else {
        viewModel.basic_life = undefined;
      }

      // Map supplemental life insurance enrollment
      if (domainModel.supplemental_life[0] != null) {
        var domainSupplementalLife = domainModel.supplemental_life[0];
        viewModel.supplemental_life = {
          "plan_name": domainSupplementalLife.company_supplemental_life_insurance_plan.supplemental_life_insurance_plan.name,
          "beneficiary": domainSupplementalLife.suppl_life_insurance_beneficiary,
          "self_elected_amount": domainSupplementalLife.self_elected_amount,
          "spouse_elected_amount": domainSupplementalLife.spouse_elected_amount,
          "child_elected_amount": domainSupplementalLife.child_elected_amount,
          "self_condition": domainSupplementalLife.self_condition.name,
          "spouse_condition": domainSupplementalLife.spouse_condition.name
        };
      } else {
        viewModel.supplemental_life = undefined;
      }

      // Map STD enrollment
      if (domainModel.std[0] != null) {
        var domainStd = domainModel.std[0];
        viewModel.std = {
          "plan_name": domainStd.company_std_insurance.std_insurance_plan.name,
          "percentage_of_salary": domainStd.company_std_insurance.percentage_of_salary,
          "max_benefit_weekly": domainStd.company_std_insurance.max_benefit_weekly,
          "duration": domainStd.company_std_insurance.duration,
          "rate": domainStd.company_std_insurance.rate,
          "employer_contribution_percentage": domainStd.company_std_insurance.employer_contribution_percentage,
          "elimination_period_in_days": domainStd.company_std_insurance.elimination_period_in_days
        };
      } else {
        viewModel.std = undefined;
      }

      // Map LTD enrollment
      if (domainModel.ltd[0] != null) {
        var domainLtd = domainModel.ltd[0];
        viewModel.ltd = {
          "plan_name": domainLtd.company_ltd_insurance.ltd_insurance_plan.name,
          "percentage_of_salary": domainLtd.company_ltd_insurance.percentage_of_salary,
          "max_benefit_monthly": domainLtd.company_ltd_insurance.max_benefit_monthly,
          "duration": domainLtd.company_ltd_insurance.duration,
          "rate": domainLtd.company_ltd_insurance.rate,
          "employer_contribution_percentage": domainLtd.company_ltd_insurance.employer_contribution_percentage,
          "elimination_period_in_months": domainLtd.company_ltd_insurance.elimination_period_in_months
        };
      } else {
        viewModel.ltd = undefined;
      }

      // Map FSA selection
      if (domainModel.fsa) {
        viewModel.fsa = {
          "primary_amount_per_year": domainModel.fsa.primary_amount_per_year,
          "dependent_amount_per_year": domainModel.fsa.dependent_amount_per_year,
          "update_reason": domainModel.fsa.update_reason
        };
      } else {
        viewModel.fsa = undefined;
      }

      var allUndefined = _.every(_.pairs(viewModel), function(keyValue) {
        return keyValue[1] === undefined;
      });

      if (allUndefined) {
        viewModel = undefined;
      }

      return viewModel;
    };

    var getBenefitEnrollmentByUser = function(userId, companyId) {
      var deferred = $q.defer();

      PersonService.getSelfPersonInfo(userId).then(function(personInfo) {
        var personId = personInfo.id;
        PersonBenefitEnrollmentRepository.BenefitEnrollmentByPerson.get({personId: personId})
        .$promise.then(function(enrollments) {
          var viewPersonBenefits = mapPersonBenefitToViewModel(enrollments);
          deferred.resolve(viewPersonBenefits);
        }, function(error) {
          deferred.reject(error);
        });
      });

      return deferred.promise;
    };

    return{
      getBenefitEnrollmentByUser: getBenefitEnrollmentByUser
    };
}]);
