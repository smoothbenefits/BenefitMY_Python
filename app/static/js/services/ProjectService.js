var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('ProjectService',
  [ '$q',
    'utilityService',
    'ProjectRepository',
    'ContractorsService',
    function ProjectService(
      $q,
      utilityService,
      ProjectRepository,
      ContractorsService){

      var ProjectStatus = {
        Active: 'Active',
        Inactive: 'Inactive'
      };

      var ProjectsById = {};

      var invalidateProjectByIdCache = function(projectId) {
        ProjectsById[projectId] = null;
      };

      var mapViewModelToDomainModel = function(viewModel){
        var domainModel = angular.copy(viewModel);
        return domainModel;
      }

      var mapDomainModelToViewModel = function(domainModel){
          var viewModel = angular.copy(domainModel);

          // Format payable created time for views
          var viewPayables = _.map(viewModel.payables, function(payable) {
            return mapPayableDomainModelToViewModel(payable);
          });

          viewModel.payables = viewPayables;
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
        if(ProjectsById[projectId]){
          var deferred = $q.defer();
          deferred.resolve(ProjectsById[projectId]);
          return deferred.promise;
        }
        else{
          return ProjectRepository.ById.get({projectId: projectId})
          .$promise.then(function(project){
            var retrievedProject = mapDomainModelToViewModel(project);
            ProjectsById[retrievedProject._id] = retrievedProject;
            return retrievedProject;
          });
        }
      };

      var GetProjectsByCompany = function(companyId){
        var compId = utilityService.getEnvAwareId(companyId);
        return ProjectRepository.ByCompany.query({compId: compId})
            .$promise.then(function(projects){
                var viewList = mapDomainModelListToViewModelList(projects);
                _.each(viewList, function(viewProject){
                  ProjectsById[viewProject._id] = viewProject;
                });
                return viewList;
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
                var createdProject = mapDomainModelToViewModel(createdModel);
                invalidateProjectByIdCache(createdProject._id);
                return createdProject;
            });
        }
        else{
          return ProjectRepository.ById.update(
            {projectId:project._id},
            domainModel)
            .$promise.then(function(updatedEntry){
              var updatedProject = mapDomainModelToViewModel(updatedEntry);
              invalidateProjectByIdCache(updatedProject._id);
              return updatedProject;
            });
        }
      };

      var SetProjectStatus = function(project, status){
        return ProjectRepository.StatusById.update(
          {projectId: project._id},
          {status: status})
          .$promise.then(function(updatedEntry){
            var updatedProject = mapDomainModelToViewModel(updatedEntry);
            invalidateProjectByIdCache(updatedProject._id);
            return updatedProject;
          });
      };

      var GetBlankProjectPayable = function(projectId) {
        var payable = {
          amount: 0,
          contractor: '',
          updatedTime: moment(),
          dateStart: moment(),
          dateEnd: moment()
        }

        return payable;
      };

      var mapPayableViewModelToDomainModel = function(viewModel){
        var domainModel = angular.copy(viewModel);
        domainModel.contractor = viewModel.contractor._id;
        return domainModel;
      }

      var mapPayableDomainModelToViewModel = function(domainModel){
          var viewModel = angular.copy(domainModel);
          viewModel.startDate = 
            moment(viewModel.dateStart)
              .add(moment().zone(), 'minutes')
                .format(SHORT_DATE_FORMAT_STRING);
          viewModel.endDate = 
            moment(viewModel.dateEnd)
              .add(moment().zone(), 'minutes')
                .format(SHORT_DATE_FORMAT_STRING);
          return viewModel;
      };

      var SaveProjectPayable = function(projectId, payable) {
        var domainModel = mapPayableViewModelToDomainModel(payable);

        // If payable has _id assigned, update existing payable
        if (payable._id) {
          return ProjectRepository.PayableByProjectPayable
          .update({projectId: projectId, payableId: payable._id}, domainModel)
          .$promise.then(function(updatedPayable) {
            invalidateProjectByIdCache(projectId);
            return mapPayableDomainModelToViewModel(updatedPayable);
          });
        } else {
          // If not, create a new payable for the project
          return ProjectRepository.PayableByProjectId.save({projectId: projectId}, domainModel)
          .$promise.then(function(savedPayable) {
            invalidateProjectByIdCache(projectId);
            return mapPayableDomainModelToViewModel(savedPayable);
          });
        }
      };

      var DeletePayableByProjectPayable = function(projectId, payable) {
        return ProjectRepository.PayableByProjectPayable.delete({projectId: projectId, payableId: payable._id})
        .$promise.then(function(response) {
          invalidateProjectByIdCache(projectId);
          return true;
        }).catch(function(err) {
          return false;
        });
      };

      // Project defines required certificates
      // Return all required types of insurance that do not cover given payment period
      var GetAllExpiredCertificatesOfRequiredInsurance = function(contractor, paymentStart, paymentEnd, project) {
        var requiredInsuranceTypes = project.requiredInsuranceTypes;

        // No required insurance type specified means no insurance required
        if (!requiredInsuranceTypes || requiredInsuranceTypes.length <= 0) {
          return [];
        }

        // If no contractor selected, return empty array
        if (!contractor) {
          return [];
        }

        var insurances = contractor.insurances;

        // If a contractor does not have insurance policy, display warning message to admin
        if (!insurances || insurances.length === 0) {
          return requiredInsuranceTypes;
        }

        // Iterate through all required insurance types,
        // determine if there is any policy which covers the entire payment period
        var expiredInsuranceTypes = [];
        var start = moment(paymentStart);
        var end = moment(paymentEnd);
        _.each(requiredInsuranceTypes, function(insuranceType) {
          var hasValid = _.some(insurances, function(insurance) {
            return moment(insurance.policy.endDate).isAfter(end) &&
              moment(insurance.policy.startDate).isBefore(start) &&
              insurance.type === insuranceType;
          });

          if (!hasValid) {
            expiredInsuranceTypes.push(insuranceType);
          }
        });

        return expiredInsuranceTypes;
      };

      return {
        ProjectStatus: ProjectStatus,
        GetProjectsByCompany: GetProjectsByCompany,
        GetBlankProject: GetBlankProject,
        SaveProject: SaveProject,
        SetProjectStatus: SetProjectStatus,
        GetProjectById: GetProjectById,
        GetBlankProjectPayable: GetBlankProjectPayable,
        SaveProjectPayable: SaveProjectPayable,
        DeletePayableByProjectPayable: DeletePayableByProjectPayable,
        GetAllExpiredCertificatesOfRequiredInsurance: GetAllExpiredCertificatesOfRequiredInsurance
      };
   }
]);
