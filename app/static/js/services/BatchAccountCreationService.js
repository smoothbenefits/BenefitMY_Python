var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'BatchAccountCreationService',
   ['$q', 'BatchAccountCreationDataParseRepository',
   function($q, BatchAccountCreationDataParseRepository){

        var mapParseDataViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.send_email = viewModel.sendEmail;
            domainModel.raw_data = viewModel.rawData;

            return domainModel;
        };

        var parseRawData = function(companyId, batchAddUserModel) {
            var model = mapParseDataViewToDomainModel(batchAddUserModel);

            var deferred = $q.defer();

            BatchAccountCreationDataParseRepository.ByCompany.save({company_id: companyId}, model).$promise.then(function(response){
                deferred.resolve(response);
            }, function(error) {
                deferred.reject(error);
            });

            return deferred.promise;
        };

        return{
            parseRawData: parseRawData
        };
   }
]);
