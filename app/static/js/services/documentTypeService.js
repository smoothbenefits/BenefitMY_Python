var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'documentTypeService',
  ['$q','documentRepository',
   function($q, documentRepository){
    return {

      getDocumentTypes: function(companyId) {
        var deferred = $q.defer();

        documentRepository.type.get({companyId:companyId})
          .$promise.then(
          function(response){
            deferred.resolve(response.document_types);
          },
          function(error) {
            deferred.reject(error);
          }
        );

        return deferred.promise;
      }

    };
  }]);
