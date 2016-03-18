var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'BatchAccountCreationService',
   ['$q', 
    'BatchAccountCreationDataParseRepository',
    'BatchAccountCreationBatchCreateRepository',
    'CompanyPersonnelsService',
   function($q, 
            BatchAccountCreationDataParseRepository,
            BatchAccountCreationBatchCreateRepository,
            CompanyPersonnelsService){

        var mapParseDataViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.send_email = viewModel.sendEmail;
            domainModel.raw_data = viewModel.rawData;

            return domainModel;
        };

        var mapBatchSaveAccountsViewToDomainModel = function(viewModel) {
            var domainModel = [];

            for (var i = 0; i < viewModel.parseDataResult.output_data.length; i++) {
                var parsedAccountResult = viewModel.parseDataResult.output_data[i];
                domainModel.push(parsedAccountResult.output_data);
            }
            
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

        var saveAllAccounts = function(companyId, batchAddUserModel) {
            var model = mapBatchSaveAccountsViewToDomainModel(batchAddUserModel);

            var deferred = $q.defer();

            BatchAccountCreationBatchCreateRepository.ByCompany.save({company_id: companyId}, model).$promise.then(function(response){
                deferred.resolve(response);
                CompanyPersonnelsService.clearCache(companyId);
            }, function(error) {
                deferred.reject(error);
            });

            return deferred.promise;
        };

        return{
            parseRawData: parseRawData,
            saveAllAccounts: saveAllAccounts
        };
   }
]);
