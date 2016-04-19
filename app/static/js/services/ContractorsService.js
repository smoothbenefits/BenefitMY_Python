var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('ContractorsService',
  [ '$q',
    'utilityService',
    'ContractorsRepository',
    function ContractorsService(
      $q,
      utilityService,
      ContractorsRepository){
      
      var ContractorStatus = {
        Active: 'Active',
        Deactivated: 'Deactivated'
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

      var GetContractorsByCompany = function(companyId){
        var compId = utilityService.getEnvAwareId(companyId);
        return ContractorsRepository.ByCompany.query({compId: compId})
            .$promise.then(function(contractors){
                return mapDomainModelListToViewModelList(contractors);
            });
      };

      var GetBlankContractor = function(companyId){
        var contractor = {
          companyDescriptor: utilityService.getEnvAwareId(companyId),
          name: '',
          contact: {
            firstName: '',
            lastName: '',
            email: '',
            phone: ''
          },
          address: {
            address1: '',
            address2: '',
            city: '',
            state: '',
            zip: ''
          },
          status: ContractorStatus.Active,
          insurances: []
        };
        return contractor;
      };

      var SaveContractor = function(contractor){
        domainContractor = mapViewModelToDomainModel(contractor);
        if(!contractor._id){
          //This is a new contractor to save.
          return ContractorsRepository.Collection.save({}, domainContractor)
            .$promise.then(function(createdContractor){
                return mapDomainModelToViewModel(createdContractor);
            });
        }
        else{
          return ContractorsRepository.ById.update(
            {contractorId:contractor._id},
            domainContractor)
            .$promise.then(function(updatedEntry){
              return updatedEntry;
            });
        }
      };

      var SetContractorStatus = function(contractor, status){
        return ContractorsRepository.StatusById.update(
          {contractorId: contractor._id},
          {status: status})
          .$promise.then(function(updateContractor){
            return updateContractor;
          });
      };

      return {
        GetContractorsByCompany: GetContractorsByCompany,
        GetBlankContractor: GetBlankContractor,
        ContractorStatus: ContractorStatus,
        SaveContractor: SaveContractor,
        SetContractorStatus: SetContractorStatus
      }; 
   }
]);