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

      updateDirectDepositByUserId: function(directDeposit, successCallBack, errorCallBack){
        DirectDepositRepository.UpdateById.update({id: directDeposit.id}, directDeposit).$promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      },

      createDirectDepositByUserId: function(userId, directDeposit, successCallBack, errorCallBack){
        DirectDepositRepository.ByEmployeeId.post({id: userId}, directDeposit).$promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      },

      deleteDirectDepositById: function(directDeposit, successCallBack, errorCallBack){
        DirectDepositRepository.DeleteById.delete({id: directDeposit.id}, directDeposit).$promise.then(function(response){
          successCallBack(response);
        }, function(error){
          errorCallBack(error);
        });
      },

      mapViewDirectDepositToDto: function(viewDirectDeposit){
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
      },

      mapDtoToViewDirectDeposit: function(directDepositDto){
        var viewDirectDepositAccounts = [];
        _.each(directDepositDto, function(account){
          var viewModel = account.bank_account;
          viewModel.direct_deposit_id = account.id;
          viewModel.amount = Number(account.amount);
          viewModel.percentage = Number(account.percentage);
          viewModel.remainder_of_all = account.remainder_of_all;
          viewDirectDepositAccounts.push(viewModel);
        });
        return viewDirectDepositAccounts;
      }
    }
  }]);
