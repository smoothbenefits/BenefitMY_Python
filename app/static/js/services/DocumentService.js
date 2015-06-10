var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('DocumentService', 
    ['$q',
    'userDocument',
    'documentTypeService',
    function ($q, userDocument, documentTypeService) {

        var constructDocumentsToTypeMap = function(docTypes, documents) {
            var typeDocMap = {};
            
            _.each(docTypes, function(type) {
                var entry = { 'docType':type, 'document':null };

                // Append some utility function to the entries
                entry.isDocumentSigned = function() {
                    return entry.document != null 
                        && entry.document.signature != null; 
                };

                typeDocMap[type.id] = entry;
            });

            _.each(documents, function(doc) {
                typeDocMap[doc.document_type.id].document = doc;
            });

            return typeDocMap;
        };

        return {

            getAllDocumentsForCompanyUser: function(userId, companyId) {
                var deferred = $q.defer();

                var typeDocMap = {};

                documentTypeService.getDocumentTypes(companyId).then(function(docTypes){
                    userDocument.query({userId:userId})
                    .$promise.then(function(userDocs){
                        var documentsToTypeMap = constructDocumentsToTypeMap(docTypes, userDocs);
                        deferred.resolve(documentsToTypeMap);
                    },
                    function(error) {
                        deferred.reject(error);
                    });
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            }

        };
    }
]);