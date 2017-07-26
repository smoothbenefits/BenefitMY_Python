var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyJobService',
  ['$q',
    'JobRepository',
   function CompanyJobService(
    $q,
    JobRepository) {

        var GetCompanyJobs = function(companyId) {
            return JobRepository.CompanyJobsByCompany.query({companyId:companyId})
                .$promise.then(function (jobs) {
                    return jobs;
                });
        };

        var DeleteCompanyJob = function(companyJob) {
            return JobRepository.CompanyJobById.delete({id:companyJob.id})
            .$promise.then(function (response) {
                return response;
            });
        };

        var SaveCompanyJob = function(companyJob) {
            var domainSaveModel = mapCompanyJobToDomainSaveModel(companyJob);

            if (domainSaveModel.id) {
                return JobRepository.CompanyJobById.update({id:domainSaveModel.id}, domainSaveModel)
                .$promise.then(function(resultCompanyJob) {
                    return resultCompanyJob;
                });
            } else {
                return JobRepository.CompanyJobById.save(domainSaveModel)
                .$promise.then(function(resultCompanyJob) {
                    return resultCompanyJob;
                });
            }
        };

        var GetBlankCompanyJobByCompanyId = function(companyId) {
            return {
                company: companyId
            };
        };

        var mapCompanyJobToDomainSaveModel = function(viewModel) {
            return angular.copy(viewModel);
        };

        return {
            GetCompanyJobs: GetCompanyJobs,
            GetBlankCompanyJobByCompanyId: GetBlankCompanyJobByCompanyId,
            DeleteCompanyJob: DeleteCompanyJob,
            SaveCompanyJob: SaveCompanyJob
        };
    }
]);
