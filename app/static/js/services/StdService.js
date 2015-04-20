var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('StdService', 
    ['$q',
    'StdRepository',
    function ($q, StdRepository){
        return {
            getStdPlansForCompany: function(companyId) {
                var deferred = $q.defer();

                deferred.resolve([{
                    'std_insurance_plan': {'name':'omg'},
                    'percentage_of_salary': 60,
                    'max_benefit_weekly': 1000,
                    'duration_in_weeks': 12,
                    'elimination_period_in_days': 7,
                    'created_date_for_display': '2015-04-17'
                }]);

                return deferred.promise;
            },

            addPlanForCompany: function(stdPlanToSave, companyId) {
                // This should be the combination of both
                // - create the plan
                // - enroll the company for this plan
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise;
            },

            deleteCompanyStdPlan: function(companyStdPlanIdToDelete) {
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise; 
            },

            deleteStdPlansForUser: function(userId) {
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise;
            },

            enrollStdPlanForUser: function(userId, companyStdPlanToEnroll) {
                // This should be take care of 2 cases
                // - user does not have a plan. Create one for him/her
                // - user already has a plan. Update
                var deferred = $q.defer();

                deferred.resolve('abc');
                
                return deferred.promise; 
            },

            getUserEnrolledStdPlanByUser: function(userId) {
                var deferred = $q.defer();

                var companyPlan = {
                    'std_insurance_plan': {'name':'omg'},
                    'percentage_of_salary': 60,
                    'max_benefit_weekly': 1000,
                    'duration_in_weeks': 12,
                    'elimination_period_in_days': 7,
                    'created_date_for_display': '2015-04-17'
                };

                deferred.resolve({
                    'company_std_insurance':companyPlan,
                    'last_update_date_time':'2015-04-21'
                });
                
                return deferred.promise; 
            }
        }; 
    }
]);
