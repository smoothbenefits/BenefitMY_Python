var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('DocumentService',
    ['$q',
    'userDocument',
    'documentTypeService',
    function ($q, userDocument, documentTypeService) {

        return {

            getDocumentsToUserEntry: function(userId){
                var deferred = $q.defer();
                var docEntry = {};
                userDocument.query({userId:userId})
                .$promise.then(function(userDocs){
                    docEntry.documents = userDocs;
                    docEntry.hasDocument = function(){
                        return _.size(this.documents) > 0;
                    };
                    docEntry.isAllSigned = function(){
                        if(this.hasDocument()){
                            var noSignature = false;
                            _.each(this.documents, function(doc){
                                if(!doc.signature){
                                    noSignature = true;
                                }

                            });
                            return !noSignature;
                        }
                    };
                    deferred.resolve(docEntry);
                }, function(errorResponse){
                    deferred.reject(errorResponse);
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
