var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TemplateService',
    ['$q',
    'templateRepository',
    function ($q, templateRepository) {
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
                deferred.resolve(response.templates);
            });
            return deferred.promise;
        };

        var getTemplateById = function(templateId){
            var deferred = $q.defer();
            templateRepository.getById.get({id:templateId})
            .$promise.then(function(templateResponse){
                deferred.resolve(templateResponse.template);
            });
            return deferred.promise;
        };

        var updateTemplate = function(companyId, template){
            var deferred = $q.defer();
            var updateObj = {company: companyId, template: template};
            templateRepository.update.update({id: template.id}, updateObj, function(response){
                deferred.resolve(response.template);
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            return deferred.promise;
        };

        var createNewTemplate = function(companyId, template){
            var deferred = $q.defer();
            template.company = companyId;
            var createObj = {company: companyId, template: template};
            templateRepository.create.save(createObj, function(response){
                deferred.resolve(response.template);
            }, function(errorResponse){
                deferred.reject(errorResponse);
            });
            return deferred.promise;
        };

        return{
            getTemplateCount: getTemplateCount,
            getAllTemplateFields: getAllTemplateFields,
            getTemplates: getTemplates,
            getTemplateById: getTemplateById,
            updateTemplate: updateTemplate,
            createNewTemplate: createNewTemplate
        };
    }
]);