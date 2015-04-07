var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('employeePayrollService', 
  ['$q', 
   'employeeTaxRepository',
   'profileSettings', 
   function ($q,
             employeeTaxRepository,
             profileSettings){

     return {
		getEmployeeTaxByUserId: function(userId){
		  var deferred = $q.defer();

		  employeeTaxRepository.get({userId: userId}).$promise.then(function(response){
		  	var fields = [];

		  	var pairs = _.pairs(response);
			var validFields = _.findWhere(profileSettings, {name: 'w4'}).valid_fields;
			_.each(pairs, function(pair){
				var key = pair[0];
				var inSetting = _.findWhere(validFields, {name: key});
				if (inSetting){
				  if (inSetting.datamap){
				    var value = pair[1];
				    var mappedValue = _.find(inSetting.datamap, function(map){
				      return map[0] === value.toString();
				    });
				    if (!mappedValue){
				      inSetting.value = 'UNKNOWN';
				    } else{
				      inSetting.value = mappedValue[1];
				    }
				  } else{
				    inSetting.value = pair[1];
				  }
				  fields.push(inSetting);
				}
			});

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