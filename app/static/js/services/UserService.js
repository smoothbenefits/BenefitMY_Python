var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('UserService', 
  ['currentUser',
   'clientListRepository',
   '$location',
   '$q',
  function (currentUser, clientListRepository, $location, $q){
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
    return {
      getCurUserInfo: function() {
        var deferred = $q.defer();
        var userInfo = {};
        currentUser.get().$promise.then(function(response){
            userInfo.user=response.user;
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
      },
      getCurrentRole: getCurRoleFromPath
    };
}]);
