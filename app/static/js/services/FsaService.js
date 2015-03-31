var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory(
  'FsaService', 
  ['FsaRepository',
  function (FsaRepository){
    return {
      getFsaElectionForUser: function(user_id, callBack) {

        FsaRepository.ByUser.get({userId:user_id})
          .$promise.then(function(existingFsa){

            var userFsa = existingFsa;

            userFsa.primary_amount_per_year = parseFloat(userFsa.primary_amount_per_year);
            userFsa.dependent_amount_per_year = parseFloat(userFsa.dependent_amount_per_year);
            userFsa.last_update_date_time = moment(userFsa.updated_at).format(DATE_FORMAT_STRING);

            if (callBack) {
              callBack(userFsa);
            }
          },
          function(failedResponse){
            if (failedResponse.status === 404) {
              // Didn't locate FSA record for the user, return a shell one 
              var shellFsa = { user:user_id, primary_amount_per_year:0, dependent_amount_per_year:0 };

              if (callBack) {
                callBack(shellFsa);
              }
            }
          });
      },

      saveFsaElection: function(fsaElectionToSave, successCallBack, errorCallBack) {
        if(!fsaElectionToSave.id) {
          // New one, POST it
          // TODO: have to give a dummy ID for now to match the URL rules, 
          // can this be eliminated?
          FsaRepository.ById.save({id:fsaElectionToSave.user}, fsaElectionToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }  
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
        else {
          // Existing, PUT it 
          FsaRepository.ById.update({id:fsaElectionToSave.id}, fsaElectionToSave
            , function (successResponse) {
                if (successCallBack) {
                  successCallBack(successResponse);
                }  
              }
            , function(errorResponse) {
                if (errorCallBack) {
                  errorCallBack(errorResponse);
              }
          });
        }
      }
    }; 
  }
]);
