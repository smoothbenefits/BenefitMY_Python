var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'DirectDepositService',
  ['$q',
   'currentUser',
   'DirectDepositRepository',
  function($q,
           currentUser,
           DirectDepositRepository){

    var deleteDirectDepositById = function(directDeposit){
      var deferred = $q.defer();

      DirectDepositRepository.DeleteById.delete({id: directDeposit.id}, directDeposit).$promise.then(function(response){
        deferred.resolve(response);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var updateDirectDepositById = function(directDeposit){
      var deferred = $q.defer();

      DirectDepositRepository.UpdateById.update({id: directDeposit.id}, directDeposit).$promise.then(function(response){
        deferred.resolve(response);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var createDirectDepositByUserId = function(userId, directDeposit){
      var deferred = $q.defer();

      DirectDepositRepository.ByEmployeeId.post({id: userId}, directDeposit).$promise.then(function(response){
        deferred.resolve(response);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var getEmptyDirectDepositAccount = function(){
      var deferred = $q.defer();
      var account = {
        account_type: 'Checking',
        bank_name: '',
        routing: '',
        account: '',
        amount: 0,
        percentage: 100,
        remainder_of_all: false
      };

      currentUser.get().$promise.then(function(response){
        account.user = response.user.id;
        deferred.resolve(account);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var getDirectDepositByUserId = function(userId){
      var deferred = $q.defer();
      DirectDepositRepository.ByEmployeeId.query({id: userId}).$promise.then(function(response){
        deferred.resolve(response);
      }, function(error){
        deferred.reject(error);
      });

      return deferred.promise;
    };

    var mapViewDirectDepositToDto = function(viewDirectDeposit){
      var dto = {
        id: viewDirectDeposit.direct_deposit_id,
        user: viewDirectDeposit.user,
        bank_account: viewDirectDeposit,
        amount: viewDirectDeposit.amount,
        percentage: viewDirectDeposit.percentage,
        remainder_of_all: viewDirectDeposit.remainder_of_all
      };
      dto.bank_account.user = viewDirectDeposit.user;
      return dto;
    };

    var mapDtoToViewDirectDeposit = function(account){
      var viewModel = account.bank_account;
      viewModel.direct_deposit_id = account.id;
      viewModel.amount = Number(account.amount);
      viewModel.percentage = Number(account.percentage);
      viewModel.remainder_of_all = account.remainder_of_all;
      if (account.remainder_of_all){
        viewModel.remainder_of_all_readable = 'Yes';
      }
      else{
        viewModel.remainder_of_all_readable = 'No';
      }
      return viewModel;
    };

    var mapDtoToViewDirectDepositInBulk = function(dtos){
      var viewDirectDepositAccounts = [];
      _.each(dtos, function(account){
        var viewModel = mapDtoToViewDirectDeposit(account);
        viewDirectDepositAccounts.push(viewModel);
      });
      return viewDirectDepositAccounts;
    }

    return {
      getDirectDepositByUserId: getDirectDepositByUserId,

      updateDirectDepositById: updateDirectDepositById,

      createDirectDepositByUserId: createDirectDepositByUserId,

      deleteDirectDepositById: deleteDirectDepositById,

      getEmptyDirectDepositAccount: getEmptyDirectDepositAccount,

      mapViewDirectDepositToDto: mapViewDirectDepositToDto,

      mapDtoToViewDirectDeposit: mapDtoToViewDirectDeposit,

      mapDtoToViewDirectDepositInBulk: mapDtoToViewDirectDepositInBulk
    }
  }]);
