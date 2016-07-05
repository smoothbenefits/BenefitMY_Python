var benefitmyService = angular.module('benefitmyService');

var API_PREFIX = '/api/v1';

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

      var InsuranceCertificateTypes = [
        'Commercial General Liability',
        'Umbrella Liability',
        'Excess Liability',
        'Worker\'s Compensation and Employee Liability'
      ];

      var mapViewModelToDomainModel = function(viewModel){
        var domainModel = angular.copy(viewModel);
        return domainModel;
      }

      var mapDomainModelToViewModel = function(domainModel){
          var viewModel = angular.copy(domainModel);
          _.each(viewModel.insurances, function(insurance){
            insurance.policy.endDateDisplay = moment(insurance.policy.endDate).format('MMM Do YYYY');
          });
          return viewModel;
      };

      var mapDomainModelListToViewModelList = function(domainModelList){
          var viewModelList = [];
          _.each(domainModelList, function(domainModel){
              viewModelList.push(mapDomainModelToViewModel(domainModel));
          });
          return viewModelList;
      };

      var GetContractorById = function(contractorId){
        return ContractorsRepository.ById.get({contractorId: contractorId})
          .$promise.then(function(contractor){
            return mapDomainModelToViewModel(contractor);
          });
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

      var GetBlankInsuranceCertificate = function(contractorId){
        var insuranceCertificate = {
          type: '',
          agent : {
            name: '',
            contact: '',
            address: '',
            email: '',
            phone: ''
          },
          policy: {
            policyNumber: '',
            startDate: '',
            endDate: '',
            coveredAmount: ''
          },
          uploads: []
        };
        return insuranceCertificate;
      };

      var SaveInsuranceCertificate = function(contractorId, insuranceCertificate){
        return ContractorsRepository.InsuranceCertificates.save(
          {contractorId: contractorId},
          insuranceCertificate)
          .$promise.then(function(updatedContractor){
            return updatedContractor;
          });
      };

      var DeleteInsuranceCertificate = function(contractorId, insuranceCertificateId){
        return ContractorsRepository.InsuranceCertificateById.delete(
          {contractorId: contractorId, insuranceCertificateId: insuranceCertificateId})
          .$promise.then(function(){
            return true;
          }, function(error){
            return error;
          });
      };

      var GetLienWaiverDownloadUrl = function(companyId, contractorId) {
        return API_PREFIX + '/company/' + companyId + '/contractors/' + contractorId + '/forms/lien_waiver';
      };

      return {
        GetContractorsByCompany: GetContractorsByCompany,
        GetBlankContractor: GetBlankContractor,
        ContractorStatus: ContractorStatus,
        SaveContractor: SaveContractor,
        SetContractorStatus: SetContractorStatus,
        GetBlankInsuranceCertificate: GetBlankInsuranceCertificate,
        SaveInsuranceCertificate: SaveInsuranceCertificate,
        DeleteInsuranceCertificate: DeleteInsuranceCertificate,
        GetContractorById: GetContractorById,
        InsuranceCertificateTypes: InsuranceCertificateTypes,
        GetLienWaiverDownloadUrl: GetLienWaiverDownloadUrl
      };
   }
]);
