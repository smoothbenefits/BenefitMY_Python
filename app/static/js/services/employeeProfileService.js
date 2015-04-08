var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('employeeProfileService', 
  ['$q', 
   'employmentAuthRepository',
   'profileSettings', 
   function($q,
            employmentAuthRepository,
            profileSettings){

     return {
     	getEmploymentAuthSummaryByUserId: function(userId){
     		var deferred = $q.defer();

     		employmentAuthRepository.get({userId: userId}).$promise.then(function(response){
     			var rawType = response.worker_type;
     			var section = _.findWhere(profileSettings, {name: 'i9'});
     			var datamap = _.findWhere(section.valid_fields, {name: 'worker_type'}).datamap;
     			var type = _.find(datamap, function(map){
     				return map[0] === rawType;
     			});
     			var info = {worker_type: type[1]};

     			deferred.resolve(info);
     		}, function(error){
     			deferred.reject(response);
     		});

     		return deferred.promise;
     	},

       	getEmploymentAuthByUserId: function(userId){
        	var deferred = $q.defer();

			employmentAuthRepository.get({userId: userId}).$promise.then(function(response){
				var fields = [];

			  	var pairs = _.pairs(response);
				var validFields = _.findWhere(profileSettings, {name: 'i9'}).valid_fields;
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

   		saveEmploymentAuthByUserId: function(employee, signature){
   			var deferred = $q.defer();
   			var contract = {
   				'worker_type': employee.auth_type,
		        'uscis_number': employee.authNumber,
		        'i_94': employee.I94Id,
		        'passport': employee.passportId,
		        'country': employee.passportCountry,
		        'signature': {
		          'signature': signature,
		          'signature_type': 'work_auth'
		        }
   			};

   			if (employee.auth_expiration){
   				contract.expiration_date = moment(employee.auth_expiration).format('YYYY-MM-DD');
   			}

   			employmentAuthRepository.save({userId: employee.userId}, contract).$promise.then(function(response){
   				deferred.resolve(response);
   			}, function(error){
   				deferred.reject(error);
   			});

   			return deferred.promise;
   		}
   	};
   }
  ]);
