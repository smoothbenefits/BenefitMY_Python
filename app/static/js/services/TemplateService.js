var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TemplateService',
    ['$q',
    'templateRepository',
    function ($q, templateRepository) {
        var contentTypes = {
            text: 1,
            upload: 2
        };

        var mapDomainToViewModel = function(domainModel) {
            if (!domainModel) {
                return domainModel;
            }

            var viewModel = {};

            viewModel.id = domainModel.id;
            viewModel.company = domainModel.company;
            viewModel.name = domainModel.name;
            viewModel.content = domainModel.content;
            viewModel.fields = domainModel.fields;
            viewModel.upload = domainModel.upload;
            viewModel.contentType = viewModel.upload 
                                    ? contentTypes.upload
                                    : contentTypes.text;

            return viewModel;
        };

        var mapViewToDomainModel = function(viewModel) {
            if (!viewModel) {
                return viewModel;
            }

            var domainModel = {};

            domainModel.id = viewModel.id;
            domainModel.company = viewModel.company
                                ? viewModel.company.id
                                : null;
            domainModel.name = viewModel.name;
            domainModel.content = viewModel.content;
            domainModel.fields = viewModel.fields;
            domainModel.upload = viewModel.upload 
                                ? viewModel.upload.id
                                : null;

            return domainModel;
        };

        var getTemplateCount = function(companyId){
            var deferred = $q.defer();
            templateRepository.byCompany.get({companyId:companyId}).$promise.then(function(response){
                deferred.resolve(_.size(response.templates));
            });
            return deferred.promise;
        };

        var getAllTemplateFields = function(companyId){
            var deferred = $q.defer();
            templateRepository.getAllFields.query({id:companyId})
            .$promise.then(function(fields){
                deferred.resolve(fields);
            });
            return deferred.promise;
        };

        var getTemplates = function(companyId){
            var deferred = $q.defer();
            templateRepository.byCompany.get({companyId:companyId})
            .$promise.then(function(response){
                var templates = null;
                if (response && response.templates) {
                    templates = [];
                    _.each(response.templates, function(item) {
                        templates.push(mapDomainToViewModel(item));
                    });
                }
                deferred.resolve(templates);
            });
            return deferred.promise;
        };

        var getTemplateById = function(templateId){
            var deferred = $q.defer();
            templateRepository.getById.get({id:templateId})
            .$promise.then(function(templateResponse){
                deferred.resolve(mapDomainToViewModel(templateResponse.template));
            });
            return deferred.promise;
        };

        var updateTemplate = function(companyId, template){
            var deferred = $q.defer();
            var templateDomainModel = mapViewToDomainModel(template);
            var updateObj = {company: companyId, template: templateDomainModel};
            templateRepository.update.update({id: templateDomainModel.id}, updateObj, function(response){
                deferred.resolve(mapDomainToViewModel(response.template));
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            return deferred.promise;
        };

        var createNewTemplate = function(companyId, template){
            var deferred = $q.defer();
            var templateDomainModel = mapViewToDomainModel(template);
            templateDomainModel.company = companyId;
            var createObj = {company: companyId, template: templateDomainModel};
            templateRepository.create.save(createObj, function(response){
                deferred.resolve(mapDomainToViewModel(response.template));
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            return deferred.promise;
        };

        return{
            contentTypes: contentTypes,
            getTemplateCount: getTemplateCount,
            getAllTemplateFields: getAllTemplateFields,
            getTemplates: getTemplates,
            getTemplateById: getTemplateById,
            updateTemplate: updateTemplate,
            createNewTemplate: createNewTemplate
        };
    }
]);