var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('LtdService', 
    ['$q',
    'LtdRepository',
    function ($q, LtdRepository){
        return {
            getLtdPlansForCompany: function(companyId) {
                var deferred = $q.defer();

                deferred.resolve([{
                    'ltd_insurance_plan': {'name':'omg_ltd'},
                    'percentage_of_salary': 60,
                    'max_benefit_monthly': 6000,
                    'duration_in_weeks': 60,
                    'elimination_period_in_days': 7,
                    'created_date_for_display': '2015-04-20'
                }]);

                return deferred.promise;
            },

            addPlanForCompany: function(ltdPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise;
            },

            deleteCompanyLtdPlan: function(companyLtdPlanIdToDelete) {
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise; 
            },

            deleteLtdPlansForUser: function(userId) {
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise;
            },

            enrollLtdPlanForUser: function(userId, companyLtdPlanToEnroll) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise; 
            },

            getUserEnrolledLtdPlanByUser: function(userId) {
                var deferred = $q.defer();

                var companyPlan = {
                    'ltd_insurance_plan': {'name':'omg_ltd'},
                    'percentage_of_salary': 60,
                    'max_benefit_monthly': 6000,
                    'duration_in_weeks': 60,
                    'elimination_period_in_days': 7,
                    'created_date_for_display': '2015-04-20'
                };

                deferred.resolve({
                    'company_ltd_insurance':companyPlan,
                    'last_update_date_time':'2015-04-21'
                });
                
                return deferred.promise; 
            }
        }; 
    }
]);
