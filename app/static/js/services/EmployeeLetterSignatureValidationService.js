var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('EmployeeLetterSignatureValidationService',
  ['documentRepository',
  function(documentRepository){
    return function(employeeId, letterType, success, failure){
      documentRepository.byUser.query({userId:employeeId})
        .$promise.then(function(response){
          var letter = _.find(response, function(l){
            return l.document_type.name === letterType;
          });
          if(!letter && success){
            success();
          }
          else if(letter.signature && letter.signature.signature && success){
            success();
          }
          else if(failure){
            failure();
          }
        })
    };
  }]);
