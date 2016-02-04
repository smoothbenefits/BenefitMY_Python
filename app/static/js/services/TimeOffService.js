var benefitmyService = angular.module('benefitmyService');

benefitmyService.factory('TimeOffService',
  ['$q',
   'envService',
   'TimeOffRepository',
   function TimeOffService(
    $q,
    envService,
    TimeOffRepository){
        var _GetEnvAwareId = function(id){
            var env = envService.get();
            return env + '_' + id;
        };

        var mapDomainModelsToViewModels = function(domainModels){
            var viewModels = [];
            _.each(domainModels, function(domainModel){
                var viewModel = {
                    type: domainModel.type,
                    duration: domainModel.duration,
                    start: moment(domainModel.startDateTime).format(DATE_TIME_FORMAT_STRING),
                    created: moment(domainModel.timeStamp).format(DATE_TIME_FORMAT_STRING)
                };
                viewModels.push(viewModel);
            });
            return viewModels;
        };

        var GetTimeOffsByRequestor = function(requestor){
            var id = _GetEnvAwareId(requestor);
            return TimeOffRepository.ByRequestor.query({userId:id})
                .$promise.then(function(timeoffs){
                    return mapDomainModelsToViewModels(timeoffs);
                });
        };

        return {
            GetTimeOffsByRequestor: GetTimeOffsByRequestor
        };
    }
]);