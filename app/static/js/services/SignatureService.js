var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('SignatureService',
    ['$q',
    'SignatureRepository',
    function ($q, SignatureRepository){

        var mapSignatureDomainToViewModel = function(signatureDomainModel) {
            var viewModel = {};

            viewModel.id = signatureDomainModel.id;
            viewModel.signature = signatureDomainModel.signature;
            viewModel.userId = signatureDomainModel.user;
            viewModel.signatureImage = getSignatureImage(viewModel.signature);
            viewModel.createdDateForDisplay = moment(signatureDomainModel.created_at).format(DATE_FORMAT_STRING);

            return viewModel;
        };

        var mapSignatureViewToDomainModel = function(signatureViewModel) {
            var domainModel = {};

            domainModel.id = signatureViewModel.id;
            domainModel.signature = signatureViewModel.signature;
            domainModel.user = signatureViewModel.userId;

            return domainModel;
        };

        var getSignatureImage = function(signatureData) {
            if (signatureData) {
                var separator = '<?xml';
                var sigComponents = signatureData.split(separator);
                var signatureImage = sigComponents[0] + encodeURIComponent(separator + sigComponents[1]);
                return signatureImage;
            }

            return null;
        }

        return {

            getSignatureById: function(signatureId) {
                var deferred = $q.defer();

                SignatureRepository.ById.get({signatureId:signatureId})
                .$promise.then(
                    function(signature) {
                        deferred.resolve(mapSignatureDomainToViewModel(signature));
                    },
                    function(error) {
                        deferred.reject(error);
                    }
                );

                return deferred.promise;
            },

            getSignatureByUser: function(userId) {
                var deferred = $q.defer();

                SignatureRepository.ByUser.get({userId:userId})
                .$promise.then(
                    function(signature) {
                        if (!signature.id) {
                            signature = { 'user': userId };
                        }
                        deferred.resolve(mapSignatureDomainToViewModel(signature));
                    },
                    function(error) {
                        deferred.reject(error);
                    }
                );

                return deferred.promise;
            },

            saveSignature: function(signatureToSave) {
                var deferred = $q.defer();

                var domainModel = mapSignatureViewToDomainModel(signatureToSave);

                if (domainModel.id){
                    deferred.reject('The signature exists already!');
                } else {
                    SignatureRepository.ById.save(domainModel)
                    .$promise.then(function(response) {
                        deferred.resolve(mapSignatureDomainToViewModel(response));
                    },
                    function(error){
                        deferred.reject(error);
                    });
                }

                return deferred.promise;
            },
        };
    }
]);
