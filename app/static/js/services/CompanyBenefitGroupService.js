var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('CompanyBenefitGroupService', [
  '$q', 'CompanyGroupRepository', 'CompanyGroupMemberRepository',
  function($q, CompanyGroupRepository, CompanyGroupMemberRepository) {

    var mapCompanyGroupToViewModel = function(domainModel) {
      return {
        'id': domainModel.id,
        'name': domainModel.name,
        'updated': moment(domainModel.updated).format(DATE_FORMAT_STRING)
      };
    };

    var mapCompanyGroupToDomainModel = function(companyId, viewModel) {
      var domainModel = {
        'company': companyId,
        'name': viewModel.name
      };

      if (viewModel.id) {
        domainModel.id = viewModel.id;
      }

      return domainModel;
    };

    var getCompanyBenefitGroupByCompany = function(companyId) {
      return CompanyGroupRepository.ByCompany.query({companyId: companyId}).$promise
      .then(function(groups) {
        var viewModels = []
        _.each(groups, function(group) {
          viewModels.push(mapCompanyGroupToViewModel(group));
        });

        return viewModels;
      });
    };

    var addNewCompanyGroup = function(companyId, group) {
      var domainModel = mapCompanyGroupToDomainModel(companyId, group);
      // Assign random number in the URL for post method
      return CompanyGroupRepository.ById.save({groupId: companyId}, domainModel).$promise;
    };

    var updateCompanyGroup = function(companyId, group) {
      var deferred =  $q.defer();

      if (!group.id) {
        deferred.reject('Group ID is not found. Not able to update.');
      }

      var domainModel = mapCompanyGroupToDomainModel(companyId, group);
      CompanyGroupRepository.ById.update({groupId: group.id}, domainModel).$promise
      .then(function(response) {
        deferred.resolve(response);
      }, function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    }

    var deleteCompanyGroup = function(group) {
      var deferred = $q.defer();

      if (!group.id) {
        deferred.reject('Group ID is not found. Not able to update.');
      }

      CompanyGroupRepository.ById.delete({groupId: group.id}).$promise
      .then(function(response) {
        deferred.resolve(response);
      }, function(error) {
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var updateCompanyGroupMembership = function(newMemberGroup){
      var deferred = $q.defer();

      CompanyGroupMemberRepository.ById.update({groupMemberId:newMemberGroup.id}, newMemberGroup)
      .$promise.then(function(response){
        CompanyGroupMemberRepository.ById.get({groupMemberId:response.id})
        .$promise.then(function(groupMember){
          deferred.resolve(groupMember);
        });
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    }

    return {
      GetCompanyBenefitGroupByCompany: getCompanyBenefitGroupByCompany,
      AddNewCompanyGroup: addNewCompanyGroup,
      UpdateCompanyGroup: updateCompanyGroup,
      DeleteCompanyGroup: deleteCompanyGroup,
      updateCompanyGroupMembership: updateCompanyGroupMembership
    };
  }
]);
