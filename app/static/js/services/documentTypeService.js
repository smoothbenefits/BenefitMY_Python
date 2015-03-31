var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'documentTypeService',
  ['documentRepository',
   function(documentRepository){
    return {
      getDocumentTypeById: function(companyId, documentTypeId, serviceCallBack){
        documentRepository.type.get({companyId:companyId})
          .$promise.then(function(docTypeResponse){
            var docType = _.findWhere(docTypeResponse.document_types, {id:documentTypeId});
            if(serviceCallBack){
              serviceCallBack(docType);
            }
          });
      },
      getDocumentTypes: function(companyId, serviceCallBack){
        documentRepository.type.get({companyId:companyId})
          .$promise.then(function(response){
            if(serviceCallBack){
              serviceCallBack(response.document_types);
            }
          });
      }
    };
  }]);
