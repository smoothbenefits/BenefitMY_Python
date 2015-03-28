var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'DirectDepositService',
  ['DirectDepositRepository',
  function(DirectDepositRepository){
    return {
      getDirectDepositByUserId: function(userId, successCallBack, errorCallBack){
        DirectDepositRepository.ByEmployeeId.query({id: userId}).$promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      },

      updateDirectDepositByUserId: function(userId, directDeposit, successCallBack, errorCallBack){
        DirectDepositRepository.UpdateByEmployeeId.update({id: userId}, directDeposit).$promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      },

      createDirectDepositByUserId: function(userId, directDeposit, successCallBack, errorCallBack){
        DirectDepositRepository.CreateByEmployeeId.post({id: userId}, directDeposit). $promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      }
    }
  }]);
