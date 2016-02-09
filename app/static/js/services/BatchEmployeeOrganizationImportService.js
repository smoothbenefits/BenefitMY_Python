var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
   'BatchEmployeeOrganizationImportService',
   ['$q', 
    'BatchEmployeeOrganizationImportDataParseRepository',
    'BatchEmployeeOrganizationImportRepository',
   function($q, 
            BatchEmployeeOrganizationImportDataParseRepository,
            BatchEmployeeOrganizationImportRepository){

        var mapParseDataViewToDomainModel = function(viewModel) {
            var domainModel = {};

            domainModel.send_email = viewModel.sendEmail;
            domainModel.raw_data = viewModel.rawData;

            return domainModel;
        };

        var mapBatchSaveViewToDomainModel = function(viewModel) {
            var domainModel = [];

            for (var i = 0; i < viewModel.parseDataResult.output_data.length; i++) {
                var parsedResult = viewModel.parseDataResult.output_data[i];
                domainModel.push(parsedResult.output_data);
            }
            
            return domainModel;
        };

        var parseRawData = function(companyId, batchDataModel) {
            var model = mapParseDataViewToDomainModel(batchDataModel);

            return BatchEmployeeOrganizationImportDataParseRepository.ByCompany.save({company_id: companyId}, model).$promise;
        };

        var saveAll = function(companyId, batchDataModel) {
            var model = mapBatchSaveViewToDomainModel(batchDataModel);

            return BatchEmployeeOrganizationImportRepository.ByCompany.save({company_id: companyId}, model).$promise;
        };

        return{
            parseRawData: parseRawData,
            saveAll: saveAll
        };
   }
]);
