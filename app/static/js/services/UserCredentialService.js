var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserCredentialService',
  ['UserCredentialRepository',
  function (UserCredentialRepository){

    var UpdateUserCredential = function (target, newPassword) {

      var request = {
        'target': target,
        'password': newPassword
      };

      return UserCredentialRepository.update({}, request).$promise
      .then(function (response) {
        return response;
      }, function (error) {
        return error;
      });
    };

    return {
      UpdateUserCredential: UpdateUserCredential
    };
}]);
