var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('DocumentService',
    ['$q',
    'documentTypeService',
    'documentRepository',
    function ($q, documentTypeService, documentRepository) {

        var contentTypes = {
            text: 1,
            upload: 2
        };

        var mapDocumentDomainToViewModel = function(domainModel) {
            if (!domainModel) {
                return domainModel;
            }

            var viewModel = {};

            viewModel.id = domainModel.id;
            viewModel.name = domainModel.name;
            viewModel.company = domainModel.company;
            viewModel.user = domainModel.user;
            viewModel.signature = domainModel.signature;
            viewModel.upload = domainModel.upload;
            viewModel.edited = domainModel.edited;
            viewModel.content = domainModel.content;
            viewModel.contentType = viewModel.upload 
                                    ? contentTypes.upload
                                    : contentTypes.text;
            viewModel.created_at = domainModel.created_at;
            viewModel.updated_at = domainModel.updated_at;
            viewModel.createDateForDisplay = moment(domainModel.created_at).format(DATE_FORMAT_STRING);
            viewModel.updateDateForDisplay = moment(domainModel.updated_at).format(DATE_FORMAT_STRING);

            // Also prepare signature timestamp for display
            if (viewModel.signature) {
                viewModel.signature.createTimeForDisplay = moment(viewModel.signature.created_at).format(DATE_TIME_FORMAT_STRING);
            }

            // Attach document download link if it is appropriate
            if (viewModel.upload) {
                viewModel.downloadUrl = '/api/v1/documents/' + viewModel.id + '/download';
            }

            return viewModel;
        };

        var mapDocumentViewToDomainModel = function(viewModel) {
            if (!viewModel) {
                return viewModel;
            }

            var domainModel = {};

            domainModel.id = viewModel.id;
            domainModel.name = viewModel.name;
            domainModel.company = viewModel.company.id;
            domainModel.user = viewModel.user.id;
            domainModel.signature = viewModel.signature
                                    ? viewModel.signature.id
                                    : null;
            domainModel.upload = viewModel.upload
                               ? viewModel.upload.id
                               : null;
            domainModel.edited = viewModel.edited;
            domainModel.content = viewModel.content;

            return domainModel;
        };

        var mapBatchDocumentCreationViewToDomainModel = function(viewModel) {
            if (!viewModel) {
                return viewModel;
            }

            var domainModel = {};

            domainModel.document_name = viewModel.documentName;
            domainModel.template_id = viewModel.templateId;

            return domainModel;
        };

        return {
            contentTypes: contentTypes,

            getDocumentsToUserEntry: function(userId){
                var deferred = $q.defer();
                var docEntry = {};
                documentRepository.byUser.query({userId:userId})
                .$promise.then(function(userDocs){
                    var docModels = [];
                    _.each(userDocs, function(doc){
                        docModels.push(mapDocumentDomainToViewModel(doc));
                    });
                    docEntry.documents = docModels;
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

                documentRepository.byUser.query({userId:userId})
                .$promise.then(function(userDocs){
                    var docModels = [];
                    _.each(userDocs, function(doc){
                        docModels.push(mapDocumentDomainToViewModel(doc));
                    });
                    deferred.resolve(docModels);
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            getUserDocumentById: function(userId, documentId) {
                var deferred = $q.defer();

                documentRepository.byUser.query({userId:userId})
                .$promise.then(function(userDocs){
                    var doc = _.find(userDocs, function(doc)
                    {
                        return doc.id === documentId;
                    })
                    deferred.resolve(mapDocumentDomainToViewModel(doc));
                },
                function(error) {
                    deferred.reject(error);
                });

                return deferred.promise;
            },

            signUserDocument: function(documentId, signatureId) {
                var deferred = $q.defer();

                documentRepository.sign.save({id:documentId}, { 'signature_id': signatureId })
                .$promise.then(function(resultDoc){
                    deferred.resolve(mapDocumentDomainToViewModel(resultDoc));
                },
                function(errors) {
                    deferred.reject(errors);
                });

                return deferred.promise;
            },

            batchSignUserDocuments: function(documents, signatureId) {
                var requests = [];

                _.each(documents, function(document) {
                    var deferred = $q.defer();
                    requests.push(deferred);

                    documentRepository.sign.save({id:document.id}, { 'signature_id': signatureId })
                    .$promise.then(function(resultDoc){
                        deferred.resolve(mapDocumentDomainToViewModel(resultDoc));
                    },
                    function(errors) {
                        deferred.reject(errors);
                    });
                });

                return $q.all(requests);
            },

            getDocumentById: function(documentId) {
                var deferred = $q.defer();

                documentRepository.getById.get({id: documentId})
                .$promise.then(function(response){
                    deferred.resolve(mapDocumentDomainToViewModel(response));
                },
                function(errors) {
                    deferred.reject(errors);
                });

                return deferred.promise;
            },

            deleteDocumentById: function(documentId) {
                var deferred = $q.defer();

                documentRepository.getById.delete({id: documentId})
                .$promise.then(function(response){
                    deferred.resolve(response);
                },
                function(errors) {
                    deferred.reject(errors);
                });

                return deferred.promise;
            },

            updateDocumentById: function(documentId, documentViewModel) {
                var deferred = $q.defer();

                var requestModel = {
                    "company": documentViewModel.company.id,
                    "user": documentViewModel.user.id,
                    "signature": documentViewModel.signature,
                    "document": {
                      "name": documentViewModel.name,
                      "content": documentViewModel.content
                    }
                };

                documentRepository.updateById.update({id:documentViewModel.id}, requestModel)
                .$promise.then(function(resultDoc){
                  deferred.resolve(mapDocumentDomainToViewModel(resultDoc));
                },
                function(errors) {
                    deferred.reject(errors);
                });

                return deferred.promise;
            },

            createDocument: function(companyId, employeeId, templateId, signature, documentModel) {
                var deferred = $q.defer();

                var postObj={company:companyId, user:employeeId, template:templateId, signature:'', document:documentModel};
     
                documentRepository.create.save(postObj, function(resultDoc){
                    deferred.resolve(mapDocumentDomainToViewModel(resultDoc));
                }, function(errors){
                    deferred.reject(errors);
                });

                return deferred.promise;
            },

            batchCreateDocuments: function(companyId, batchCreateDocumentModel) {
                var domainModel = mapBatchDocumentCreationViewToDomainModel(batchCreateDocumentModel);

                var deferred = $q.defer();
     
                documentRepository.byCompany.save({companyId:companyId}, domainModel)
                .$promise.then(function(resultDocs){
                    var docs = [];
                    _.each(resultDocs, function(resultDoc) {
                        docs.push(mapDocumentDomainToViewModel(resultDoc));    
                    });
                    deferred.resolve(docs);
                }, function(errors){
                    deferred.reject(errors);
                });

                return deferred.promise;
            },
        };
    }
]);
