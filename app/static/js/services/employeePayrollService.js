var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('employeePayrollService',
  ['$q',
   'employeeTaxRepository',
   'utilityServcie',
   'profileSettings',
   function ($q,
             employeeTaxRepository,
             utilityServcie,
             profileSettings){

    var getMarriageNumber = function(withholdingType){
      if (withholdingType === 'married'){
        return 2;
      }
      else if(withholdingType === 'higher'){
        return 1;
      }
      else{
        return 0;
      }
    };

    return {
      getEmployeeTaxSummaryByUserId: function(userId){
        var deferred = $q.defer();

        employeeTaxRepository.get({userId: userId}).$promise.then(function(response){
          deferred.resolve(response);
        }, function(error){
          deferred.reject(error);
        });

        return deferred.promise;
      },

      mapW4DtoToView: function(w4Dto){
        var viewW4 = {};
        viewW4.withholdingType = 'single';
        if(w4Dto.marriage === 2){
          viewW4.withholdingType = 'married';
        }
        else if(w4Dto.marriage === 1){
          viewW4.withholdingType = 'higher';
        }
        viewW4.headOfHousehold = w4Dto.head;
        viewW4.extra_amount = parseFloat(w4Dto.extra_amount);
        viewW4.dependent_count = w4Dto.dependencies;
        viewW4.childExpense = w4Dto.tax_credit;
        viewW4.user_defined_points = w4Dto.user_defined_points;
        viewW4.calculated_points = w4Dto.calculated_points;
        return viewW4;
      },

      mapW4ViewToDto: function(viewW4){
        var w4Dto = {
          marriage: getMarriageNumber(viewW4.withholdingType),
          dependencies: viewW4.dependent_count,
          head: viewW4.headOfHousehold,
          tax_credit: viewW4.childExpense,
          calculated_points: viewW4.calculated_points,
          user_defined_points: viewW4.user_defined_points,
          extra_amount: viewW4.extra_amount
        };
        return w4Dto;
      },

      calculateTotalBasedOnViewW4: function(viewW4){
        var total = getMarriageNumber(viewW4.withholdingType);
        if (total === 0){
          total ++ ;
        }
        total += viewW4.dependent_count;
        if(viewW4.childExpense && total){
          total += parseInt(viewW4.childExpense);
        }
        if(viewW4.headOfHousehold && total){
          total += parseInt(viewW4.headOfHousehold);
        }
        if(!total)
        {
          total = undefined;
        }
        viewW4.calculated_points = total;
        if(!viewW4.user_defined_set){
          viewW4.user_defined_points = viewW4.calculated_points;
        }
        return total;
      },

      saveEmployeeTaxByUserId: function(userId, request){
        var deferred = $q.defer();
        employeeTaxRepository.save({userId:userId}, request).$promise.then(function(response){
          deferred.resolve(response);
        }, function(error){
          deferred.reject(error);
        });

        return deferred.promise;
      },

      getMarriageNumberForUser: getMarriageNumber
    }
  }
]);
