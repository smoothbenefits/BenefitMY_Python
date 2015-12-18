var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserService',
  ['currentUser',
   'clientListRepository',
   'users',
   '$location',
   '$q',
  function (currentUser, clientListRepository, users, $location, $q){
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

    var getUserDataByUserId = function(userId) {
        var deferred = $q.defer();

        users.get({userId:userId}).$promise.then(
            function(userData) {
                deferred.resolve(userData);
            },
            function(errors) {
                deferred.reject(errors);
            }
        );

        return deferred.promise;
    };

    return {
      getCurUserInfo: getCurUserInfo,
      getCurrentRole: getCurRoleFromPath,
      isCurrentUserNewEmployee: isCurrentUserNewEmployee,
      getUserDataByUserId: getUserDataByUserId
    };
}]);
