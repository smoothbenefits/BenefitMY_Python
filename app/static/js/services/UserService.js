var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserService',
  ['currentUser',
   'clientListRepository',
   'users',
   '$location',
   '$q',
   'CompanyFeatureService',
  function (
    currentUser,
    clientListRepository,
    users,
    $location,
    $q,
    CompanyFeatureService){

    var getCurRoleFromPath = function(){
        var curPath = $location.path();
        if(curPath[0] === '/'){
            curPath = curPath.substring(1);
        }
        var pathArray = curPath.split('/');
        if(pathArray.length > 0){
            return pathArray[0];
        }
        else{
            return undefined;
        }
    };
    var getCurUserInfo = function() {
        var deferred = $q.defer();
        var userInfo = {};
        currentUser.get().$promise.then(function(response){
            userInfo.user = response.user;
            userInfo.roles = response.roles;
            userInfo.person = response.person;
          clientListRepository.get({userId: response.user.id})
            .$promise.then(function(response){
            var curRole = _.find(response.company_roles, {company_user_type: getCurRoleFromPath()});
            if(curRole){
              userInfo.currentRole = curRole;
            }
            else{
              //we cannot find the curRole from path, what can we do?
              //we will select the first role from the list then.
              userInfo.currentRole = response.company_roles[0];
            }
            deferred.resolve(userInfo);
          });
        });
        return deferred.promise;
    };
    var isCurrentUserNewEmployee = function() {
        var deferred = $q.defer();

        getCurUserInfo().then(
            function(userInfo) {
                var result = false;
                var employeeRole = _.findWhere(userInfo.roles, {company_user_type:'employee'});
                if(employeeRole && employeeRole.new_employee) {
                    result = true;
                }
                deferred.resolve(result);
            },
            function(errors) {
                deferred.reject(errors);
            }
        );

        return deferred.promise;
    };

    var mapUserToServiceModel = function(domainUser){
      var viewUser = domainUser.user;
      //Here we assume a user only is connected to only 1 company group, 
      //though our data domain allows a user to be connected to multiple company group
      viewUser.companyGroupId = null;
      if(domainUser.user.company_group_user && domainUser.user.company_group_user.length > 0)
      {
        viewUser.companyGroupId = domainUser.user.company_group_user[0].company_group.id
      }
      return viewUser;
    };

    var getUserDataByUserId = function(userId) {
        var deferred = $q.defer();

        users.get({userId:userId}).$promise.then(
            function(userData) {
                var viewUser = mapUserToServiceModel(userData);
                deferred.resolve(viewUser);
            },
            function(errors) {
                deferred.reject(errors);
            }
        );

        return deferred.promise;
    };

    var getCurrentRoleCompleteFeatureStatus = function() {
        return getCurUserInfo().then(function(userInfo) {
            var userId = userInfo.user.id;
            var companyId = userInfo.currentRole.company.id;
            return CompanyFeatureService.getAllApplicationFeatureStatusByCompanyUser(companyId, userId);
        });
    };

    return {
      getCurUserInfo: getCurUserInfo,
      getCurrentRole: getCurRoleFromPath,
      isCurrentUserNewEmployee: isCurrentUserNewEmployee,
      getUserDataByUserId: getUserDataByUserId,
      getCurrentRoleCompleteFeatureStatus: getCurrentRoleCompleteFeatureStatus
    };
}]);
