var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmploymentProfileService',
  ['$q',
   'employmentAuthRepository',
   'utilityServcie',
   'profileSettings',
   function($q,
            employmentAuthRepository,
            utilityServcie,
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
           deferred.reject(error);
         });

         return deferred.promise;
       },

       getEmploymentAuthByUserId: function(userId){
        var deferred = $q.defer();

        employmentAuthRepository.get({userId: userId}).$promise.then(function(response){
          var fields = utilityServcie.mapObjectToKeyPairArray('i9', response);
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
            'signature': signature
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
