var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('ProjectService',
  [ '$q',
    'utilityService',
    'ProjectRepository',
    function ProjectService(
      $q,
      utilityService,
      ProjectRepository){
      
      var ProjectStatus = {
        Active: 'Active',
        Inactive: 'Inactive'
      };

      var mapViewModelToDomainModel = function(viewModel){
        var domainModel = angular.copy(viewModel);
        return domainModel;
      }

      var mapDomainModelToViewModel = function(domainModel){
          var viewModel = angular.copy(domainModel);
          return viewModel;
      };

      var mapDomainModelListToViewModelList = function(domainModelList){
          var viewModelList = [];
          _.each(domainModelList, function(domainModel){
              viewModelList.push(mapDomainModelToViewModel(domainModel));
          });
          return viewModelList;
      };

      var GetProjectById = function(projectId){
        return ProjectRepository.ById.get({projectId: projectId})
          .$promise.then(function(project){
            return mapDomainModelToViewModel(project);
          });
      };

      var GetProjectsByCompany = function(companyId){
        var compId = utilityService.getEnvAwareId(companyId);
        return ProjectRepository.ByCompany.query({compId: compId})
            .$promise.then(function(projects){
                return mapDomainModelListToViewModelList(projects);
            });
      };

      var GetBlankProject= function(companyId){
        var project = {
          companyDescriptor: utilityService.getEnvAwareId(companyId),
          name: '',
          address: {
            address1: '',
            address2: '',
            city: '',
            state: '',
            zip: ''
          },
          status: ProjectStatus.Active,
          requiredInsuranceTypes: [],
          payables: [],
          isCCIP: false
        };
        return project;
      };

      var SaveProject = function(project){
        domainModel = mapViewModelToDomainModel(project);
        if(!project._id){
          //This is a new model to save.
          return ProjectRepository.Collection.save({}, domainModel)
            .$promise.then(function(createdModel){
                return mapDomainModelToViewModel(createdModel);
            });
        }
        else{
          return ProjectRepository.ById.update(
            {projectId:project._id},
            domainModel)
            .$promise.then(function(updatedEntry){
              return updatedEntry;
            });
        }
      };

      var SetProjectStatus = function(project, status){
        return ProjectRepository.StatusById.update(
          {projectId: project._id},
          {status: status})
          .$promise.then(function(updateProject){
            return updateProject;
          });
      };

      return {
        ProjectStatus: ProjectStatus,

        GetProjectsByCompany: GetProjectsByCompany,
        GetBlankProject: GetBlankProject,
        SaveProject: SaveProject,
        SetProjectStatus: SetProjectStatus,
        GetProjectById: GetProjectById
      }; 
   }
]);