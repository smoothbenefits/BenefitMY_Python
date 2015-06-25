var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('DocumentService', 
    ['$q',
    'userDocument',
    'documentTypeService',
    function ($q, userDocument, documentTypeService) {

        var constructDocumentsToTypeMap = function(docTypes, documents) {
            var mapModel = {};
            mapModel.entries = {};
            
            _.each(docTypes, function(type) {
                var entry = { 'docType':type, 'documents': [] };

                // Append some utility function to the entries
                entry.isSigned = function() {
                    return entry.hasDocument()
                        && entry.documents[0].signature != null;
                };

                entry.hasDocument = function() {
                    return entry.documents != null 
                        && entry.documents.length > 0;
                };

                mapModel.entries[type.id] = entry;
            });

            _.each(documents, function(doc) {
                mapModel.entries[doc.document_type.id].documents.push(doc);
            });

            // sort (descending) each bucket by the documents' created date
            _.each(mapModel.entries, function(entry) {
                entry.documents = _.sortBy(entry.documents, function(document) {
                    if (!document.created_at) {
                        return 1000;
                    }
                    var date = new Date(document.created_at);
                    return -date;
                });
            });

            return mapModel;
        };

        return {

            getDocumentToTypeMappingForCompanyUser: function(userId, companyId) {
                var deferred = $q.defer();

                documentTypeService.getDocumentTypes(companyId).then(function(docTypes){
                    userDocument.query({userId:userId})
                    .$promise.then(function(userDocs){
                        var mapModel = constructDocumentsToTypeMap(docTypes, userDocs);
                        deferred.resolve(mapModel);
                    },
                    function(error) {
                        deferred.reject(error);
                    });
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            getAllDocumentsForUser: function(userId) {
                var deferred = $q.defer();

                userDocument.query({userId:userId})
                .$promise.then(function(userDocs){
                    deferred.resolve(userDocs);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            getUserDocumentById: function(userId, documentId) {
                var deferred = $q.defer();

                userDocument.query({userId:userId})
                .$promise.then(function(userDocs){
                    var doc = _.find(userDocs, function(doc)
                    {
                        return doc.id === documentId;
                    })
                    deferred.resolve(doc);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            }
        };
    }
]);