var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserCredentialService',
  ['UserCredentialRepository', '$q',
  function (UserCredentialRepository, $q){

    var UpdateUserCredential = function (initiator, target, newPassword) {
      var deferred = $q.defer();

      var request = {
        'target': target,
        'initiator': initiator,
        'password': newPassword
      };

      UserCredentialRepository.update({}, request).$promise
      .then(function (response) {
        deferred.resolve(response);
      }, function (error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    return {
      UpdateUserCredential: UpdateUserCredential
    };
}]);
