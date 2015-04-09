var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('employeePayrollService', 
  ['$q', 
   'employeeTaxRepository',
   'utilityServcie', 
   'profileSettings', 
   function ($q,
             employeeTaxRepository,
             utilityServcie
             profileSettings){

    return {
      getEmployeeTaxSummaryByUserId: function(userId){
        var deferred = $q.defer();

        employeeTaxRepository.get({userId: userId}).$promise.then(function(response){
          deferred.resolve(response);
        }, function(error){
          deferred.reject(response);
        });

        return deferred.promise;
      },

      getEmployeeTaxByUserId: function(userId){
        var deferred = $q.defer();

        employeeTaxRepository.get({userId: userId}).$promise.then(function(response){
          var fields = utilityServcie.mapObjectToKeyPairArray('w4', response);
          deferred.resolve(fields);
        }, function(error){
          deferred.reject(error);
        });

        return deferred.promise;
      },

      saveEmployeeTaxByUserId: function(userId, employee){
        var deferred = $q.defer();

        var request = {
          marriage: employee.marriage,
          dependencies: employee.dependent_count,
          head: employee.headOfHousehold,
          tax_credit: employee.childExpense,
          calculated_points: employee.calculated_points,
          user_defined_points: employee.user_defined_points,
          extra_amount: employee.extra_amount
        };

        employeeTaxRepository.save({userId:userId}, request).$promise.then(function(response){
          deferred.resolve(response);
        }, function(error){
          deferred.reject(error);
        });

        return deferred.promise;
      },

      getMarriageNumberForUser: function(withholdingType){
        if (withholdingType === 'married'){
          return 2;
        } 
        else{
          return 1;
        }
      }
    }  
  }
]);